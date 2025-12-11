import random 

def ask_yes_no(prompt):
    """Ask the user a Yes/No question and return True for Yes, False for No."""
    while True:
        answer = input(prompt).strip().lower()
        if answer == "yes":
            return True
        elif answer == "no":
            return False
        else:
            print("Please answer with Yes or No.")


def load_question_bank(path):
    """
    Read the question bank file and return a list of (question, answer) pairs.
    """
    try:
        file = open(path, "r", encoding="utf-8")
    except FileNotFoundError:
        print("Sorry, I could not find the file at that path.")
        return []

    lines = file.readlines()
    file.close()

    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.rstrip("\n"))

    pairs = []
    index = 0
    while index + 1 < len(cleaned_lines):
        question = cleaned_lines[index]
        answer = cleaned_lines[index + 1]
        pairs.append((question, answer))
        index += 2

    return pairs


def get_valid_question_count(max_pairs):
    while True:
        try:
            value_str = input(
                f"How many question-answer pairs do you want to include in your exam? "
                f"(1 to {max_pairs}) "
            )
            value = int(value_str)
            if 1 <= value <= max_pairs:
                return value
            else:
                print(f"Please enter a number between 1 and {max_pairs}.")
        except ValueError:
            print("Please enter a valid integer number.")


def select_random_pairs(pairs, count):
    """
    Select 'count' unique random pairs from the list 'pairs' using randint().
    We avoid repeating questions.
    """
    selected_pairs = []
    # available_indices will contain all possible indexes at the beginning
    available_indices = list(range(len(pairs)))

    for _ in range(count):
        max_position = len(available_indices) - 1
        random_position = random.randint(0, max_position)
        pair_index = available_indices.pop(random_position)
        selected_pairs.append(pairs[pair_index])

    return selected_pairs


def save_exam(output_path, selected_pairs):
    try:
        out_file = open(output_path, "w", encoding="utf-8")
    except OSError:
        print("Sorry, I could not open the output file for writing.")
        return False

    # Write each question and answer on separate lines, like the question bank
    for question, answer in selected_pairs:
        out_file.write(question + "\n")
        out_file.write(answer + "\n")

    out_file.close()
    return True


def main():
    print("Welcome to professor assistant version 1.0.")
    professor_name = input("Please Enter Your Name: ").strip()

    print(
        f"Hello Professor. {professor_name}, "
        f"I am here to help you create exams from a question bank."
    )

    while True:
        wants_exam = ask_yes_no(
            "Do you want me to help you create an exam (Yes to proceed | No to quit the program)? "
        )

        if not wants_exam:
            print(f"Thank you professor {professor_name}. Have a good day!")
            break

        # Ask for question bank path and try to load it
        question_bank_path = input(
            "Please Enter the Path to the Question Bank. "
        ).strip()

        pairs = load_question_bank(question_bank_path)

        if len(pairs) == 0:
            print("The file could not be loaded or did not contain any question-answer pairs.")

            continue

        print("Yes, the path you provided includes questions and answers.")
        max_pairs = len(pairs)
        question_count = get_valid_question_count(max_pairs)
        output_file_name = input("Where do you want to save your exam? ").strip()
        selected_pairs = select_random_pairs(pairs, question_count)
        success = save_exam(output_file_name, selected_pairs)

        if success:
            print(
                f"Congratulations Professor {professor_name}. "
                f"Your exam is created and saved in {output_file_name}."
            )
        else:
            print("Sorry, I could not save the exam file.")
if __name__ == "__main__":
    main()
