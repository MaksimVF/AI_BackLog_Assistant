





from agents.analyzers.text_cleaner import TextCleaner
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def test_text_cleaner():
    cleaner = TextCleaner()

    # Test case 1: Basic cleaning
    text1 = "  Это  пример! Текста,   с   пунктуацией...  "
    result1 = cleaner.clean(text1, log_trace=True)
    print("Test Case 1 - Basic Cleaning:")
    print(f"Original: '{text1}'")
    print(f"Cleaned: '{result1['cleaned']}'")
    print(f"Language: {result1['language']}")
    print(f"Stats: {result1['length_original']} -> {result1['length_cleaned']} chars")
    print("---")

    # Test case 2: Custom configuration
    custom_config = {
        "remove_special_chars": False,
        "lowercase": False,
        "remove_extra_spaces": True,
        "preserve_punctuation": [".", ",", "!", "?"]
    }
    cleaner2 = TextCleaner(custom_config)
    text2 = "  Keep THIS! Text, with... punctuation.  "
    result2 = cleaner2.clean(text2)
    print("Test Case 2 - Custom Configuration:")
    print(f"Original: '{text2}'")
    print(f"Cleaned: '{result2['cleaned']}'")
    print("---")

    # Test case 3: List cleaning
    texts = [
        "  First text!  ",
        "  Second, text...  ",
        "  Third!  "
    ]
    results = cleaner.clean_list(texts)
    print("Test Case 3 - List Cleaning:")
    for i, result in enumerate(results):
        print(f"Text {i+1}: '{result['cleaned']}'")
    print("---")

    # Test case 4: Tokenization
    text4 = "This is a simple tokenization test"
    tokens = cleaner.tokenize(text4)
    print("Test Case 4 - Tokenization:")
    print(f"Tokens: {tokens}")
    print("---")

    # Test case 5: Processing trace
    text5 = "Important document for processing"
    result5 = cleaner.clean(text5)
    trace = cleaner.log_processing_trace(text5, result5)
    print("Test Case 5 - Processing Trace:")
    print(f"Input: {trace['input']}")
    print(f"Output: {trace['output']}")
    print(f"Language: {trace['language']}")
    print(f"Stats: {trace['stats']}")
    print("---")

if __name__ == "__main__":
    test_text_cleaner()





