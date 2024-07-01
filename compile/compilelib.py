import re
   
add_dep_line = "##add_dependencies="

class CompilationError(Exception):
   pass

def strip_all_whitespace(input_string):
    return re.sub(r'\s+', '', input_string)

def remove_duplicates(strings_list):
    seen = set()
    result = []
    for string in strings_list:
        if string not in seen:
            result.append(string)
            seen.add(string)
    return result

def extract_strings(input_str):
    strings = []
    start_quote = None
    current_string = []

    for char in input_str:
        if char in ["'", '"']:
            if start_quote is None:
                start_quote = char
            elif start_quote == char:
                strings.append(''.join(current_string))
                current_string = []
                start_quote = None
        elif start_quote is not None:
            current_string.append(char)

    return strings


def prefilter_compilation_v2(code, headers, dist_name):
   original_format = list
   if isinstance(code, str):
      original_format = str
      code = code.split("\n")

   delete_indexes = set()

   def get_indent(line):
      return len(line) - len(line.lstrip())

   def change_indent(range1, range2, factor):
      for line_num in range(range1, range2+1):
         line = code[line_num]
         if factor < 0:
            factor = abs(factor)
            if len(line) < factor:
               raise CompilationError(f"Malformed line `{repr(line)}` on line number `{line_num}`")
            num_whitespace = get_indent(line)
            if num_whitespace < factor:
               raise CompilationError(f"This line `{repr(line)}` has only {num_whitespace} whitespace(s) but trying to change indent by {factor} spaces.")
            # hello new line
            code[line_num] = line[factor:]
         else:
            code[line_num] = " "*factor + line


   criteria = {"headers": "if{} COMPILATION.get_headers(", "dist": "if{} COMPILATION.is_dist("}
   prior_if_statement = False
   index = 0
   while index < len(code):
      line = code[index]
      index += 1

      processed_line = line.strip()

      if processed_line == "":
         continue

      if processed_line == "import COMPILATION":
         delete_indexes.add(index-1)
         continue


      # optimize: use something else in this step
      match_criteria = None
      match_key = ""

      for key, value in criteria.items():
         if processed_line.startswith(value.format("")):
            match_criteria = ""
            match_key = str(key)
            break
         elif processed_line.startswith(value.format(" not")):
            match_criteria = " not"
            match_key = str(key)
            break

      if match_criteria != None:
         match_string = criteria[match_key].format(match_criteria)
         target_strings = extract_strings(processed_line[len(match_string):])

         do_filter = False

         for target in target_strings:
             if match_key == "headers":
                 if (match_criteria.strip() != "not" and target not in headers) or (match_criteria.strip() == "not" and target in headers):
                     do_filter = True
                     break
             elif match_key == "dist":
                 if (match_criteria.strip() != "not" and target != dist_name) or (match_criteria.strip() == "not" and target == dist_name):
                     do_filter = True
                     break

         ## match the full section
         section_start = index
         section_end = section_start+1
         current_indent = get_indent(code[section_start])
         print(f"STRT: {code[section_start]}")
         while section_end < len(code):
            print(f"SECT: {code[section_end]}")
            if get_indent(code[section_end]) <= current_indent:
               break
            section_end += 1

         if do_filter: #go byebye lines
            # more efficient way of doing this
            for subnum in range(section_start, section_end+1):
               delete_indexes.add(subnum)
         else: # the lines were valid this whole time apparently
            delete_indexes.add(index)
            change_indent(section_start, section_end, -1*current_indent)

         # skip the index
         index = section_end
      else:
         continue

   code = [line for i, line in enumerate(code) if i not in delete_indexes]
   
   if original_format == list:
      return "\n".join(code)
   return code
   
      

def prefilter_compilation(code, headers, dist):
   original_inst = list
   if isinstance(code, str):
      original_inst = str
      code = code.split("\n")
   filter_ranges = set()
   get_headers = "if COMPILATION.get_headers("
   match_headers = "if COMPILATION.match_headers("
   get_dist = "if COMPILATION.is_dist("

   #code = code_str.split("\n")
   num = -1

   while num+1 < len(code):
      num += 1
      line = code[num]
      #print(f"PROC: {line}")
      do_filter_following = False
      
      if line.strip() == "import COMPILATION":
         filter_ranges.add(num)
         continue
      line_start_h = line.strip().startswith(get_headers)
      line_start_d = line.strip().startswith(get_dist)
      line_start_m = line.strip().startswith(match_headers)
      if line_start_h or line_start_d or line_start_m:
         strings = []
         if line_start_h:
            strings = extract_strings(line.strip()[len(get_headers):])
         elif line_start_d:
            strings = extract_strings(line.strip()[len(get_dist):])
         elif line_start_m:
            strings = extract_strings(line.strip()[len(match_headers):])
         if line_start_h:
            for string in strings:
               if string not in headers:
                  do_filter_following = True
                  break
         elif line_start_d:
            if len(strings) > 0 and strings[0] == dist:
               do_filter_following = True
         elif line_start_m:
            do_filter_following = True
            for string in strings:
               if string in headers:
                  do_filter_following = False
                  break
                     
         if do_filter_following:
            # destroy all indents
            current_indent = count_leading_spaces(line)
            filter_ranges.add(num)
            skip = num+1
            while skip < len(code):
               skip_line = code[skip]
               if strip_all_whitespace(skip_line) != "":
                  if count_leading_spaces(skip_line) <= current_indent:
                     break
               #print(f"DELT:{skip_line}")
               filter_ranges.add(skip)
               skip += 1
            num = skip-1
            #print("####REMAINING:")
            #print("\n".join(code[num:]))
            #print(f"NUM: {num} | LEN: {len(code)}")
         else: 
            # dedent the line
            current_indent = count_leading_spaces(line)
            filter_ranges.add(num)
            skip = num+1
            indent_diff = count_leading_spaces(code[skip])-current_indent
            
            # find ranges of lines first
            while skip < len(code):
               skip_line = code[skip]
               
               if strip_all_whitespace(skip_line) == "":
                  skip += 1
                  continue
               if count_leading_spaces(skip_line) <= current_indent:
                  break
               skip += 1

            #print(f"Indent difference: {indent_diff}")
            # from num+1 to skip describes dedentable lines
            for count in range(num+1, skip):
               line = code[count] 
               if len(line) < indent_diff:
                  continue
               code[count] = line[indent_diff:]
               #print(code[count])


   #print("####: RESULT")
   
   # filter the ranges
   new_lines = []

   for count, line in enumerate(code):
      if count in filter_ranges:
         continue
      #print(line)
      new_lines.append(line)
   if original_inst == str:
      new_lines = "\n".join(new_lines)
   return new_lines
def count_leading_spaces(s):
 string = s.rstrip()
 return len(string) - len(string.lstrip(' '))

def strip_imports(code):
   dependencies = []
   lines = []
   for num, line in enumerate(code.split("\n")):
      stripped_line = line.strip()
      if stripped_line.startswith(add_dep_line) or stripped_line.startswith("pass"+add_dep_line):
         gap = ""
         if stripped_line.startswith("pass"):
            gap = "pass"
         dependencies = stripped_line[len(gap+add_dep_line):].split(",")
      if stripped_line == "" or stripped_line.startswith("#"):
         continue
      leading_spaces = count_leading_spaces(line)
      if leading_spaces == 0:
         line_split = line.split(" ")
         if line_split[0] in ["from", "import"]:
            continue
      lines.append(line)

   for count, dep in enumerate(dependencies):
      dependencies[count] = dep.strip()
   return "\n".join(lines), dependencies 
      