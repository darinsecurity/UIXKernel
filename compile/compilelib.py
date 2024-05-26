import re
   
add_dep_line = "##add_dependencies="

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


def prefilter_compilation(code, headers, dist):
   original_inst = list
   if isinstance(code, str):
      original_inst = str
      code = code.split("\n")
   filter_ranges = set()
   get_headers = "if COMPILATION.get_headers("
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
      if line_start_h or line_start_d:
         strings = []
         if line_start_h:
            strings = extract_strings(line.strip()[len(get_headers):])
         elif line_start_d:
            strings = extract_strings(line.strip()[len(get_dist):])
         if line_start_h:
            for string in strings:
               if string not in headers:
                  do_filter_following = True
                  break
         elif line_start_d:
            if len(strings) > 0 and strings[0] == dist:
               do_filter_following = True
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
      