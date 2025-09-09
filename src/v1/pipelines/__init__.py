

"""
AI Backlog Assistant Pipelines

This package contains the pipeline architecture for coordinating AI agents:
- Base pipeline functionality
- Input Processing Pipeline (IPP)
- Information Manipulation Pipeline (IMP)
- Output Pipeline (OP)
- Main pipeline coordinator
"""

from .base_pipeline import BasePipeline, PipelineConfig
from .input_processing_pipeline import InputProcessingPipeline, IPPInputSchema, IPPOutputSchema
from .information_manipulation_pipeline import InformationManipulationPipeline, IMPInputSchema, IMPOutputSchema
from .output_pipeline import OutputPipeline, OPInputSchema, OPOutputSchema
from .main_pipeline_coordinator import MainPipelineCoordinator

__all__ = [
    'BasePipeline',
    'PipelineConfig',
    'InputProcessingPipeline',
    'IPPInputSchema',
    'IPPOutputSchema',
    'InformationManipulationPipeline',
    'IMPInputSchema',
    'IMPOutputSchema',
    'OutputPipeline',
    'OPInputSchema',
    'OPOutputSchema',
    'MainPipelineCoordinator'
]

