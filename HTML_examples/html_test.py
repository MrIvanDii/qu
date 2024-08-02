import os
from requests_html import HTMLSession
import re


def read_html_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
#
#
# def process_html_file(html_content):
#     session = HTMLSession()
#     # Вы можете обработать html_content здесь или вернуть его
#     response = session.get('data:text/html,' + html_content)
#     response.html.render(sleep=5)
#     return response.html.html


def process_html_files_in_folder(folder_path):
    # print(os.listdir(folder_path))
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)
            # print(file_path)
            html_content = read_html_from_file(file_path)
            check_answers(html_content=html_content)
            # processed_content = process_html_file(html_content)
            # print(f"Processed content from {filename}:\n{processed_content}\n")


def check_answers(html_content):
    answers_pattern_2 = r'mixRankedAnswersCount\s*["\\:\s]*\s*(\d+)'
    answers_pattern = r'decanonicalizedAnswerCount\s*["\\:\s]*\s*(\d+)'

    num_answers_match = re.search(answers_pattern_2, html_content)
    decanonicalized_count_match = re.search(answers_pattern, html_content)

    if num_answers_match:
        num_answers = num_answers_match.group(1)
        print(f"Number of answers: {num_answers}")
    else:
        print("numAnswers not found")

    if decanonicalized_count_match:
        decanonicalized_count = decanonicalized_count_match.group(1)
        print(f"Decanonicalized Answer Count: {decanonicalized_count}")
    else:
        print("decanonicalizedAnswerCount not found")


if __name__ == "__main__":
    folder_answers_path = '/Users/martinanikola/PycharmProjects/PropshtScrapping_V2/HTML_examples/answers_related_ans/'
    process_html_files_in_folder(folder_answers_path)
