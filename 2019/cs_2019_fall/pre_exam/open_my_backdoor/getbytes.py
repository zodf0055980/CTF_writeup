i = b'd00r'
j = b'exec'
print(bytes([i ^ j for i, j in zip(i, j)]))