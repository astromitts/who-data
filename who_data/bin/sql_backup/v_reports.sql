select 
	country.id as country_id,
	country.name as country_name,
	country.url_name as country_url_name,
	disease.id as disease_id,
	disease.name as disease_name,
	disease_report.year, 
	disease_report.report_count as count
from datastore.disease_report
	join datastore.country on disease_report.country_id = country.id
	join datastore.disease on disease_report.disease_id = disease.id
where disease_report.report_count is not null
;