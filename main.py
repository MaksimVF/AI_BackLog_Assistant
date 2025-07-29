

from agents.reflection_agent import ReflectionAgent, ReflectionInput
from memory.weaviate_client import WeaviateMemory
from schemas import VideoData, AudioData, ImageData, DocumentData, TextData

def main():
    # Initialize components
    memory = WeaviateMemory()
    reflection_agent = ReflectionAgent()

    # Example usage
    print("Welcome to the Multi-Agent System!")

    # Create sample data
    sample_video = VideoData(
        id="video_001",
        content="path/to/video.mp4",
        duration=120.5,
        resolution="1920x1080"
    )

    # Store in memory
    memory.store_data(
        data_id=sample_video.id,
        data_type=sample_video.data_type,
        content=sample_video.content,
        metadata=sample_video.dict()
    )

    # Process with reflection agent
    input_data = ReflectionInput(
        data_type=sample_video.data_type,
        content=sample_video.content
    )

    result = reflection_agent.process(input_data)

    print("\nReflection Agent Analysis:")
    print(f"Data Type: {input_data.data_type}")
    print(f"Analysis: {result.analysis}")
    print(f"Required Agents: {result.required_agents}")
    print(f"Recommended Tasks: {result.recommended_tasks}")

    # Update memory with processing results
    memory.update_processing_status(
        data_id=sample_video.id,
        status="analyzed",
        agents=result.required_agents
    )

    print("\nProcessing complete!")

if __name__ == "__main__":
    main()

