import sys

def fully_contained_pairs(pairs):
  count = 0
  # Go through each pair of ranges
  for pair in pairs:
    # Split the pair into two ranges
    range1, range2 = pair.split(',')
    # Split each range into a starting and ending value
    start1, end1 = map(int, range1.split('-'))
    start2, end2 = map(int, range2.split('-'))
    # Check if one range fully contains the other
    if (start1 >= start2 and end1 <= end2) or (start1 <= start2 and end1 >= end2):
      # If it does, increment the count
      count += 1
  # Return the final count
  return count

# Example input
pairs = [
  "2-4,6-8",
  "2-3,4-5",
  "5-7,7-9",
  "2-8,3-7",
  "6-6,4-6",
  "2-6,4-8"
]

# Find the number of pairs where one range fully contains the other
result = fully_contained_pairs(pairs)

# Print the result
print(result)

result = fully_contained_pairs(sys.stdin.read().split())

# Print the result
print(result)
