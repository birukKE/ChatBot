

names = ["Alexa","Siri","Cortana", "Debra", "Dexter", "Batista"]
# print(" ".join("Hello there ",(i for i in names)))

str = " ".join( "I know " + name if i%2 == 0 else "I don't know " + name for i , name in enumerate(names))

print(str)