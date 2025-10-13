# Exploring Bias in AI Compensation Models

## Overview

This project investigates how large language models handle sensitive demographic attributes when tasked with compensation estimation. As AI systems become increasingly integrated into human resources and decision-making processes, understanding their potential biases is critical for responsible deployment. Moreover, we are looking for an effective way to demonstrate how a user's prompt could influence an LLM's response.

## Motivation

Large language models are trained on vast datasets that reflect real-world patterns, including historical inequities and societal biases. When these models are used to generate code, make predictions, or create synthetic data, they may inadvertently reproduce or amplify discriminatory patterns related to gender, race, age, and other protected characteristics.

This project examines whether and how LLMs encode compensation biases by observing their behavior across two scenarios:
- Implementing compensation calculation logic based on demographic attributes
- Generating synthetic employee datasets with compensation values

## Research Questions

- Do different LLMs exhibit systematic biases when estimating compensation based on demographic factors?
- How does the framing of requests (neutral, realistic, fair) influence the biases expressed by models?
- Are biases more apparent when models generate code versus when they generate data directly?
- Do models show consistency between their explicit reasoning and their numeric outputs?
- Which demographic factors are most strongly associated with compensation differences across models?

## Scope and Limitations

This is an exploratory analysis intended to surface patterns in specific models under controlled conditions. The findings are limited to:
- The specific LLMs tested
- The particular prompts and framings used
- The demographic attributes and ranges defined in the study

Results should not be generalized to all AI systems or interpreted as definitive measurements of model bias. Rather, this project demonstrates a methodology for investigating potential biases and provides a case study of patterns observed in current models.

## Intended Use

This project serves multiple purposes:
- **Educational**: Demonstrates experimental design for studying AI bias
- **Technical**: Showcases data generation, statistical analysis, and visualization skills
- **Critical**: Encourages thoughtful consideration of AI systems in sensitive applications

The methodology and findings may inform discussions about responsible AI development, but should not be treated as comprehensive bias audits or used to make claims about model safety for production deployment.

## Disclaimer

This project generates and analyzes hypothetical compensation data based on demographic attributes solely for research purposes. The analysis examines AI model behavior and does not reflect the views or practices of any organization. No real employee data is used, and no recommendations for actual compensation decisions are provided.