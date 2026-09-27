# Raw Data Dictionary

This document describes the variables contained in the original
raw AI4I Predictive Maintenance Dataset.

## Variable Definitions

| Variable | Data Type | Unit | Description | Example |
|---|---|---|---|---|
| UID | int64 | - | Unique identifier for each observation, ranging from 1 to 10,000. | 7866 |
| Product ID | str | - | Unique product identifier containing a quality-class prefix (L, M, or H) followed by a product-specific serial number. | L55045 |
| Type | str | - | Product quality variant: L = low, M = medium, H = high. | L |
| Air temperature [K] | float64 | Kelvin | Ambient air temperature associated with the observation. | 300.5 |
| Process temperature [K] | float64 | Kelvin | Process temperature associated with the observation. | 311.9 |
| Rotational speed [rpm] | int64 | rpm | Rotational speed of the machine during the observation. | 1383 |
| Torque [Nm] | float64 | Nm | Torque produced by the machine during the observation. | 50.5 |
| Tool wear [min] | int64 | minutes | Accumulated tool wear measured in minutes. | 35 |
| Machine failure | int64 | - | Indicates whether a machine failure occurred: 0 = no failure, 1 = failure. | 0 |
| TWF | int64 | - | Indicates a tool wear failure: 0 = no, 1 = yes. | 1 |
| HDF | int64 | - | Indicates a heat dissipation failure: 0 = no, 1 = yes. | 1 |
| PWF | int64 | - | Indicates a power failure: 0 = no, 1 = yes. | 0 |
| OSF | int64 | - | Indicates an overstrain failure: 0 = no, 1 = yes. | 0 |
| RNF | int64 | - | Indicates a random failure: 0 = no, 1 = yes. | 1 |


## Failure Code Definitions
If at least one of the following failure modes is true, the process fails and the 'machine failure' label is set to 1. If multiple failure codes are true, it is not transparent which of the failure modes has caused the process to fail.

- **TWF**: *Tool Wear Failure*. The tool will be replaced of fail at a randomly selected tool wear time between 200 & 240 mins.
- **HDF**: *Heat Dissipation Failure*. Heat dissipation causes a process failure, if the difference between air- and process temperature is below 8.6 K and the tool's rotational speed is below 1380 rpm.
- **PWF**: *Power Failure*. The product of torque and rotational speed (in rad/s) equals the power required for the process. If this power is below 3500 W or above 9000 W, the process fails.
- **OSF**: *Overstrain Failure*. If the product of tool wear and torque exceeds 11,000 minNm for the L product variant (12,000 M, 13,000 H), the process fails due to overstrain.
- **RNF**: *Random Failure*. Each process has a chance of 0.1 % to fail regardless of its process parameters.


## Data Generation Notes
The dataset contains 10,000 observations and represents a synthetic
predictive-maintenance dataset.

- **Product quality:** Products are categorized as low (L), medium (M),
  or high (H) quality variants.
- **Air temperature:** Generated using a random-walk process and
  normalized around 300 K with a standard deviation of approximately 2 K.
- **Process temperature:** Generated using a random-walk process and
  related to air temperature, with approximately 10 K added.
- **Rotational speed:** Derived using a power value of 2,860 W with
  normally distributed noise.
- **Torque:** Generated around 40 Nm with a standard deviation of
  approximately 10 Nm, with negative values excluded.
- **Tool wear:** Accumulates according to product quality variant.
- **Machine failure:** Indicates whether one or more defined machine
  failure conditions occurred.

## Known Data Quality Issues

- no missing values.
- no duplicate observations.
- 18 Observations show a individual failure flag, but Machine failure is false.
- 9 Observations show a Machine failure, but no individual failure flags are true.

## Source
Dataset comes from AI4I 2020 Predictive Maintenance Dataset.
https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset