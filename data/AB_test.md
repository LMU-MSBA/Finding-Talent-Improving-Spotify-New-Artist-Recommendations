# A/B Test Plan

## Metrics:
The objective of our A/B test is to determine which submission method—either hitting "enter" on the keyboard or clicking the visible "Submit" button after pasting the track link—more effectively increases user engagement. We will measure engagement using five key performance metrics:
- **Conversion Rate**: Main metric, indicating the percentage of visitors successfully submitting a track link. Higher rates suggest better utility of the app.
- **Number of Conversions**: Counts users who successfully submit a track link, part of calculating the conversion rate.
- **Visit Frequency**: Monitors how often users return to the app, with higher frequency suggesting greater user satisfaction.
- **Number of Unique Visitors**: Tracks the diversity of users visiting the app, with more unique visitors indicating broader appeal and growth potential.
- **Completion Time**: Measures how quickly users can complete the submission, with shorter times indicating a more intuitive UI.

## Hypotheses:
- **Null Hypothesis (H0)**: There is no difference in key performance metrics between Test A and Test B, suggesting no impact from changing the submission method.
- **Alternative Hypothesis (H1)**: The conversion rate of Test A (no submit button) is higher than Test B’s (with submit button).

## Experimental Design:
- **Group A - Control**: Users hit “enter” on their keyboard to submit their track link.
- **Group B - Experimental**: Users click the submit button on the app to submit their track link.
- **Randomization**: Users are assigned to groups using a Python script, with random values below 0.5 placing users in Group A and values above 0.5 in Group B.
- **Duration**: The test runs for two weeks to align with our sprint schedule, allowing sufficient time for evaluation.
- **Sample Size Calculation**: Utilizes Optimizely’s sample size calculator. Key metrics for calculation include a baseline conversion rate of 70%, a minimum detectable effect of 5%, and a statistical significance level of 95%. Ideal sample size would be 2000 artists per variant; realistically, we will test 100 artists due to pilot phase constraints.

## Implementation Plan:
- **Technical Setup**: Using Streamlit and Python to conduct the test.
- **Timeline**:
  - **Week 1**: Update privacy policy, develop front and backend code for randomization and UI deployment - leveraging and 50/50 random split, and conduct internal trial A/B test.
  - **Week 2-3**: Deploy A/B test, collect data, and monitor operations.
  - **Week 4**: Collect final data, review results, and evaluate statistical significance.

## Ethical Considerations:
- To ensure informed consent, we are updating our privacy policy to clearly communicate the nature of the A/B test.
- A rigorous randomization process in Python is used to minimize biases, ensuring a fair and unbiased evaluation of the outcomes.

## Data Collection and Analysis:
- **Data Collection**: Python will be used to collect user data via Streamlit during the A/B test. Data cleaning will be conducted before analysis.
- **Data Analysis**: Key performance metrics will be calculated post-test. The AB+ Test Calculator by CXL will be used to determine the significance of the results, utilizing inputs such as test duration, data per group, and baseline metrics to generate confidence intervals.

## Documentation and Review:
- Save and document all processes and results in `docs/data/AB_test.md`.
- Publish and share the findings through our GitHub repository to facilitate transparency and collaborative review.
