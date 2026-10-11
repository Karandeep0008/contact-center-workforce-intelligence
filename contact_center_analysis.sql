UPDATE contact_center_analytics.call_records
SET csat_score = NULL
WHERE csat_score = 0;
SELECT
    COUNT(*) AS total_records,
    COUNT(csat_score) AS records_with_csat,
    SUM(csat_score IS NULL) AS missing_csat
FROM contact_center_analytics.call_records;
SELECT
    COUNT(*) AS total_calls,
    SUM(call_status = 'Answered') AS answered_calls,
    SUM(call_status = 'Abandoned') AS abandoned_calls,
    ROUND(
        100.0 * SUM(call_status = 'Answered') / COUNT(*), 2
    ) AS answer_rate_pct,
    ROUND(
        100.0 * SUM(call_status = 'Abandoned') / COUNT(*), 2
    ) AS abandonment_rate_pct,
    ROUND(
        AVG(NULLIF(handling_time_seconds, 0)), 2
    ) AS avg_handling_time_seconds,
    ROUND(AVG(wait_time_seconds), 2) AS avg_wait_seconds,
    ROUND(SUM(revenue_inr), 2) AS total_revenue_inr
FROM contact_center_analytics.call_records;
SELECT
    team,
    COUNT(*) AS total_calls,
    SUM(call_status = 'Answered') AS answered_calls,
    SUM(call_status = 'Abandoned') AS abandoned_calls,
    ROUND(
        100.0 * SUM(call_status = 'Answered') / COUNT(*), 2
    ) AS answer_rate_pct,
    ROUND(
        AVG(NULLIF(handling_time_seconds, 0)), 2
    ) AS avg_handling_time_seconds,
    ROUND(AVG(wait_time_seconds), 2) AS avg_wait_seconds,
    ROUND(SUM(revenue_inr), 2) AS total_revenue_inr
FROM contact_center_analytics.call_records
GROUP BY team
ORDER BY total_calls DESC;
SELECT
    call_hour,
    COUNT(*) AS total_calls,
    SUM(call_status = 'Answered') AS answered_calls,
    SUM(call_status = 'Abandoned') AS abandoned_calls,
    ROUND(AVG(wait_time_seconds), 2) AS avg_wait_seconds,
    ROUND(
        100.0 * SUM(call_status = 'Abandoned') / COUNT(*), 2
    ) AS abandonment_rate_pct
FROM contact_center_analytics.call_records
GROUP BY call_hour
ORDER BY call_hour;
SELECT
    team,
    COUNT(*) AS total_calls,
    ROUND(AVG(csat_score), 2) AS avg_csat,
    ROUND(
        100.0 * SUM(resolved_first_contact = 1) /
        NULLIF(SUM(call_status = 'Answered'), 0),
        2
    ) AS fcr_rate_pct,
    ROUND(
        100.0 * SUM(survey_responded = 1) / COUNT(*),
        2
    ) AS survey_response_rate_pct
FROM contact_center_analytics.call_records
GROUP BY team
ORDER BY avg_csat DESC;