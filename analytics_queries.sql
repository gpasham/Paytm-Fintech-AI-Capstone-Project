-- Q1 — SELECT / WHERE / ORDER BY / LIMIT / DISTINCT
SELECT DISTINCT payment_method
FROM transactions
WHERE status = 'chargeback'
ORDER BY payment_method
LIMIT 10;

-- Q2 — Chargeback impact
SELECT
    COUNT(*) AS chargeback_transactions,
    COUNT(DISTINCT user_id) AS unique_users_affected,
    SUM(amount_inr) AS total_chargeback_amount_inr
FROM transactions
WHERE status = 'chargeback';

-- Q3 — Burner accounts (<30 days, non-negative age)
SELECT
    t.transaction_id,
    t.user_id,
    u.signup_date,
    t.transaction_time,
    CAST(julianday(t.transaction_time) - julianday(u.signup_date) AS INTEGER)
        AS account_age_days,
    t.amount_inr,
    t.status,
    t.risk_score
FROM transactions AS t
INNER JOIN users AS u ON u.user_id = t.user_id
WHERE t.status = 'chargeback'
  AND julianday(t.transaction_time) >= julianday(u.signup_date)
  AND (julianday(t.transaction_time) - julianday(u.signup_date)) >= 0
  AND (julianday(t.transaction_time) - julianday(u.signup_date)) < 30
ORDER BY t.user_id, t.transaction_time
LIMIT 100;

-- Q4 — LEFT JOIN merchant coverage
SELECT
    m.merchant_id,
    m.merchant_name,
    COUNT(t.transaction_id) AS transaction_count,
    COALESCE(SUM(t.amount_inr), 0) AS total_amount_inr
FROM merchants AS m
LEFT JOIN transactions AS t ON t.merchant_id = m.merchant_id
GROUP BY m.merchant_id, m.merchant_name
ORDER BY transaction_count DESC, m.merchant_id
LIMIT 10;

-- Q5 — Velocity, floored 10-minute buckets
WITH bucketed AS (
    SELECT
        user_id,
        transaction_id,
        transaction_time,
        datetime(
            (CAST(strftime('%s', transaction_time) AS INTEGER) / 600) * 600,
            'unixepoch'
        ) AS bucket_start
    FROM transactions
)
SELECT
    user_id,
    bucket_start,
    MIN(transaction_time) AS earliest_transaction_time,
    COUNT(*) AS transaction_count
FROM bucketed
GROUP BY user_id, bucket_start
HAVING COUNT(*) >= 3
ORDER BY user_id, bucket_start;

-- Q6 — Velocity, explicit rolling 10-minute windows
SELECT
    t1.user_id,
    t1.transaction_time AS window_start,
    COUNT(t2.transaction_id) AS transactions_in_10_min
FROM transactions AS t1
INNER JOIN transactions AS t2
    ON t2.user_id = t1.user_id
   AND julianday(t2.transaction_time) >= julianday(t1.transaction_time)
   AND julianday(t2.transaction_time) <= julianday(t1.transaction_time, '+10 minutes')
GROUP BY t1.user_id, t1.transaction_time
HAVING COUNT(t2.transaction_id) >= 3
ORDER BY t1.user_id, t1.transaction_time;

