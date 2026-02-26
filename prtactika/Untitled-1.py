# 1.
# with open("test.txt", "w", encoding="utf-8") as file:
#     file.write("Привет, файл!")
# 2.
# with open("numbers.txt", "w", encoding="utf-8") as file:
#     for i in range(1, 11):
#         file.write(f'{i}\n')
# total = 0 
# with open("numbers.txt", "r", encoding="utf-8") as file:
#     for line in file:
#         total += int(line)
# print(total)
# 3.
# with open("user_text.txt", "w", encoding="utf-8") as file:
#     for _ in range(5):
#         file.write(f'{input()} \n')
# with open("user_text.txt", "r", encoding="utf-8") as file:
#     for line in file:
#         if len(line.strip()) > 5:
#             print(line.strip())
# 4.
# with open("data.txt", "r", encoding="utf-8") as file:
#     count = 0
#     for line in file:
#         count += 1
# print(count)
# 5.
# with open ("data.txt", 'r', encoding="utf-8") as file:
#     count = 0
#     for line in file:
#         count += line.count(' ') + 1
# print(count)
# 6.
# with open('log.txt', 'a', encoding='utf-8') as file:
#     file.write('\nPYTHON')
#     file.write('\nIN')
#     file.write('\nAWESOME')
# 7.
# with open('numbers.txt', 'r', encoding='utf-8') as file:
#     count = file.read()
#     numbers = [int(i) for i in count.split()]
#     print(max(numbers))
#     print(min(numbers))
# 8.
# with open('user_text.txt', 'r', encoding='utf-8') as file:
#     count = file.read()
# with open('user_text_(1).txt', 'w', encoding='utf-8') as file:
#     file.write(count)
# 9.
# with open('user_text.txt', 'r', encoding='utf-8') as file:
#     count = file.read()
# with open('user_text_(2).txt', 'w', encoding='utf-8') as file:
#     file.write(count.upper())
# 10.
# import json
# data = {
#     "имя":"Александр",
#     "возраст":"17",
#     "город":"Ульяновск"
# }
# with open ("person.json", 'w', encoding='utf-8') as file:
#     json.dump(data, file, ensure_ascii=False, indent=4)
# with open('person.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)