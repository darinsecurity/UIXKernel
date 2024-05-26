# Lightweight datetime library in Python
# Not as large as the actual one (75 KB)
class lwdatetime:
    def get_time_difference(timestamp1, timestamp2, units):
        # Ensure timestamp1 is the smaller one
        if timestamp1 > timestamp2:
            timestamp1, timestamp2 = timestamp2, timestamp1
    
        # Calculate the difference in seconds
        total_seconds = timestamp2 - timestamp1
    
        # Dictionary to hold time unit values in seconds
        time_units = {
            'years': 31536000,  # Approximation: 365 days
            'days': 86400,
            'hours': 3600,
            'minutes': 60,
            'seconds': 1
        }
    
        # Prepare the result dictionary
        result = {}
    
        for unit in units:
            if unit in time_units:
                unit_value = time_units[unit]
                result[unit] = total_seconds // unit_value
                total_seconds %= unit_value
    
        # Print the result in the requested order
        return "The system has been up for " + ", ".join([unit + ": " + str(int(result[unit])) for unit in units])