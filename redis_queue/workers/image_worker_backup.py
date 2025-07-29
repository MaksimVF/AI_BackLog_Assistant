








import os
from tools.image2text_tool import ImageToTextTool
from tools.weaviate_storage_tool import WeaviateStorageTool

def process_image_file(image_path):
    if not os.path.exists(image_path):
        return {"error": "Image file not found"}

    # Extract text from image
    image_to_text = ImageToTextTool()
    text = image_to_text._execute(image_path)

    # Store results in Weaviate
    weaviate = WeaviateStorageTool()
    weaviate.store_chunk(
        content=text,
        source_type="image",
        source_name=os.path.basename(image_path),
        metadata={"type": "ocr"}
    )

    return {
        "image_path": image_path,
        "text_length": len(text),
        "status": "processed"
    }









