CREATE TABLE IF NOT EXISTS credits_history (
    id INT PRIMARY KEY,
    serious_dlq_in_2_yrs SMALLINT NOT NULL,
    revolving_utilization_of_unsecured_lines DOUBLE PRECISION NOT NULL,
    age SMALLINT NOT NULL,
    number_of_time_30_59_days_past_due_not_worse INT NOT NULL,
    debt_ratio DOUBLE PRECISION NOT NULL,
    monthly_income REAL,
    number_of_open_credit_lines_and_loans INT NOT NULL,
    number_of_times_90_days_late INT NOT NULL,
    number_real_estate_loans_or_lines INT NOT NULL,
    number_of_time_60_89_days_past_due_not_worse INT NOT NULL,
    number_of_dependents INT
);