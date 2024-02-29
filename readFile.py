# Open the file
# with open("Test1.txt", "r") as file, open("createFile.txt", "w") as FileWrite:
#     # data = file.read()
#     # print(data)
#     lines = file.readlines()
#     for line in lines:
#         print(f"line::\n{line}\n")
#         FileWrite.write(line)
#     FileWrite.close()
#     file.close()

def checkword():
    with open("Test1.txt", "r") as file:
        sentence = 0
        lines = file.readline()
        splitContent = lines.split('.')
        word = str(input(" Enter word:"))
        print(type(word))
        for Content in splitContent:
            if word in Content:
                sentence += 1
                print(Content)

        print(f"Total Sentence are:{sentence}")
        file.close()


if __name__ == "__main__":
    checkword()
