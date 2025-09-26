# Gerenator function that counts down from n to 1
def countdown(n):
    print("Counting down from", n)
    while n > 0:
        yield n        
        n -= 1
    print("Done!")

for i in countdown(5):
    print(f"Generator yield: n={i}")