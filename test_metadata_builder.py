



from agents.analyzers.metadata_builder import MetadataBuilder

def test_metadata_builder():
    builder = MetadataBuilder()

    # Test case 1: Basic input
    input1 = {
        "user_id": "user123",
        "text": "Как работает эта система?",
        "source": "web"
    }

    metadata1 = builder.build_metadata(input1)
    print("Test Case 1 - Basic Input:")
    print(f"Context: {metadata1['context']}")
    print(f"Intent: {metadata1['intent']}")
    print(f"Language: {metadata1['language']}")
    print(f"Domain: {metadata1['domain']}")
    print(f"Confidence: {metadata1['confidence_level']}")
    print(f"Format: {metadata1['format']}")
    print("---")

    # Test case 2: Financial context
    input2 = {
        "user_id": "user456",
        "text": "Проблемы с кредитом и выплатами",
        "source": "mobile"
    }

    metadata2 = builder.build_metadata(input2)
    print("Test Case 2 - Financial Context:")
    print(f"Context: {metadata2['context']}")
    print(f"Intent: {metadata2['intent']}")
    print(f"Domain: {metadata2['domain']}")
    print("---")

    # Test case 3: Storage format
    storage_data = builder.build_metadata_for_storage(input1)
    print("Test Case 3 - Storage Format:")
    print(f"Content: {storage_data['content']}")
    print(f"Source Type: {storage_data['source_type']}")
    print("Metadata fields:")
    for key, value in storage_data['metadata'].items():
        print(f"  {key}: {value}")
    print("---")

if __name__ == "__main__":
    test_metadata_builder()



