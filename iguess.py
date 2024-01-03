import random
from nltk.corpus import words
from nltk.metrics import edit_distance

def load_dataset(file_path):
    with open(file_path, 'r') as file:
        dataset = [line.strip() for line in file]
    return dataset

def select_word(used_words, dataset):
    available_words = [word for word in dataset if word not in used_words]
    if not available_words:
        return random.choice(dataset)
    elif used_words:
        closest_word = min(available_words, key=lambda w: edit_distance(w, used_words[-1]))
        return closest_word
    else:
        # If used_words is empty, just return a random word from the dataset
        return random.choice(dataset)

def get_user_feedback():
    return input("Is the AI's guess hot, cold, or correct? ").lower()

def retrain_dataset(dataset, correct_word, hot_words, cold_words):
    for word in dataset:
        distance = edit_distance(word, correct_word)
        if distance < 3:
            hot_words.add(word)
        elif distance > 5:
            cold_words.add(word)

def main():
    print("Welcome to the Hot and Cold Word Guessing Game!")

    dataset_file_path = '10000.txt'
    dataset = load_dataset(dataset_file_path)

    if not dataset:
        print("Error: Unable to load the dataset.")
        return

    hot_words = set()
    cold_words = set()

    while True:
        total_attempts = 0
        used_words = []

        while True:
            ai_word = select_word(used_words, dataset)
            print(f"AI's suggested word: {ai_word}")

            user_feedback = get_user_feedback()

            if user_feedback == "correct":
                print(f"Congratulations! The AI guessed the correct word '{ai_word}' in {total_attempts + 1} attempts!")
                retrain_dataset(dataset, ai_word, hot_words, cold_words)
                used_words.append(ai_word)
                break  # Exit the loop after a correct guess
            elif user_feedback == "hot":
                print("The AI's guess is hot, but it's not the correct word. Keep going!")
                hot_words.add(ai_word)
            elif user_feedback == "cold":
                used_words.append(ai_word)
                print("The AI's guess is cold. Keep going!")
                cold_words.add(ai_word)
            else:
                print("Incorrect feedback. The game continues.")

            total_attempts += 1

        print(f"Total attempts in this game: {total_attempts}")

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            break  # Exit the loop if the user doesn't want to play again

    # Saving the updated dataset after each execution
    with open('updated_dataset.txt', 'w') as file:
        file.write('\n'.join(dataset + list(hot_words) + list(cold_words)))

if __name__ == "__main__":
    main()
