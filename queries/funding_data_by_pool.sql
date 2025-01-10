SELECT to_project_name, grant_pool_name, from_project_name, sum(amount)
FROM `oso_production.oss_funding_v0`
where from_project_name in ('optimism', 'opencollective', 'gitcoin')
group by to_project_name, grant_pool_name, from_project_name