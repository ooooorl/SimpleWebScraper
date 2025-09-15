
import pandas as pd
import requests


def fetch_jobs(
    search_query: str,
    location: str = "New York, United States",
    date_past_days: int = 14,
):
    API_URL = "https://hiring.cafe/api/search-jobs"

    payload = {
        "size": 40,
        "page": 0,
        "searchState": {
            "searchQuery": search_query,
            "dateFetchedPastNDays": date_past_days,
            "locations": [
                {
                    "formatted_address": location,
                    "types": ["administrative_area_level_1"],
                    "address_components": [
                        {
                            "long_name": "New York",
                            "short_name": "NY",
                            "types": ["administrative_area_level_1"],
                        },
                        {
                            "long_name": "United States",
                            "short_name": "US",
                            "types": ["country"],
                        },
                    ],
                }
            ],
            "workplaceTypes": ["Remote", "Hybrid", "Onsite"],
            "sortBy": "default",
        },
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }

    try:
        resp = requests.post(API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        # Debug: Print response structure
        print("Response keys:", data.keys())
        print("Total results found:", len(data.get("results", [])))

        jobs = []
        # Extract comprehensive job information
        for item in data.get("results", []):
            # Basic job info
            job_info = item.get("job_information", {})
            company_data = item.get("v5_processed_company_data", {})
            processed_job_data = item.get("v5_processed_job_data", {})

            # Format salary range
            min_salary = processed_job_data.get("yearly_min_compensation", 0)
            max_salary = processed_job_data.get("yearly_max_compensation", 0)
            salary_range = (
                f"${min_salary:,.0f} - ${max_salary:,.0f}"
                if min_salary and max_salary
                else "Not specified"
            )

            # Format arrays as strings
            def format_array(arr):
                return (
                    ", ".join(arr) if isinstance(arr, list) and arr else "Not specified"
                )

            job_entry = {
                # Basic Job Information
                "job_id": item.get("id", ""),
                "job_title": job_info.get("title") or item.get("job_title_raw", ""),
                "job_title_raw": item.get("job_title_raw", ""),
                "core_job_title": processed_job_data.get("core_job_title", ""),
                "apply_url": item.get("apply_url", ""),
                "is_expired": item.get("is_expired", False),
                "source": item.get("source", ""),
                "board_token": item.get("board_token", ""),
                "requisition_id": item.get("requisition_id", ""),
                # Company Information
                "company_name": company_data.get("name", ""),
                "company_website": company_data.get("website", ""),
                "company_tagline": company_data.get("tagline", ""),
                "company_linkedin": company_data.get("linkedin_url", ""),
                "company_headquarters": company_data.get("headquarters_country", ""),
                "company_founded": company_data.get("year_founded", ""),
                "company_employees": company_data.get("num_employees", ""),
                "company_revenue": company_data.get("latest_revenue", ""),
                "company_revenue_year": company_data.get("latest_revenue_year", ""),
                "stock_symbol": company_data.get("stock_symbol", ""),
                "stock_exchange": company_data.get("stock_exchange", ""),
                "is_public_company": company_data.get("is_public_company", False),
                "company_activities": format_array(company_data.get("activities", [])),
                "company_industries": format_array(company_data.get("industries", [])),
                # Job Details & Requirements
                "job_category": processed_job_data.get("job_category", ""),
                "seniority_level": processed_job_data.get("seniority_level", ""),
                "role_type": processed_job_data.get("role_type", ""),
                "commitment": format_array(processed_job_data.get("commitment", [])),
                "workplace_type": processed_job_data.get("workplace_type", ""),
                "workplace_location": processed_job_data.get(
                    "formatted_workplace_location", ""
                ),
                "workplace_continents": format_array(
                    processed_job_data.get("workplace_continents", [])
                ),
                "workplace_countries": format_array(
                    processed_job_data.get("workplace_countries", [])
                ),
                "workplace_physical_environment": processed_job_data.get(
                    "workplace_physical_environment", ""
                ),
                # Education Requirements
                "bachelors_required": processed_job_data.get(
                    "bachelors_degree_requirement", ""
                ),
                "bachelors_fields": format_array(
                    processed_job_data.get("bachelors_degree_fields_of_study", [])
                ),
                "masters_required": processed_job_data.get(
                    "masters_degree_requirement", ""
                ),
                "masters_fields": format_array(
                    processed_job_data.get("masters_degree_fields_of_study", [])
                ),
                "doctorate_required": processed_job_data.get(
                    "doctorate_degree_requirement", ""
                ),
                "high_school_required": processed_job_data.get(
                    "is_high_school_required", False
                ),
                # Experience Requirements
                "min_industry_experience": processed_job_data.get(
                    "min_industry_and_role_yoe", ""
                ),
                "min_management_experience": processed_job_data.get(
                    "min_management_and_leadership_yoe", ""
                ),
                # Compensation
                "salary_range": salary_range,
                "yearly_min_salary": processed_job_data.get(
                    "yearly_min_compensation", ""
                ),
                "yearly_max_salary": processed_job_data.get(
                    "yearly_max_compensation", ""
                ),
                "hourly_min_salary": processed_job_data.get(
                    "hourly_min_compensation", ""
                ),
                "hourly_max_salary": processed_job_data.get(
                    "hourly_max_compensation", ""
                ),
                "compensation_currency": processed_job_data.get(
                    "listed_compensation_currency", ""
                ),
                "compensation_frequency": processed_job_data.get(
                    "listed_compensation_frequency", ""
                ),
                "is_compensation_transparent": processed_job_data.get(
                    "is_compensation_transparent", False
                ),
                # Work Conditions
                "travel_requirement_air": processed_job_data.get(
                    "air_travel_requirement", ""
                ),
                "travel_requirement_land": processed_job_data.get(
                    "land_travel_requirement", ""
                ),
                "physical_labor_intensity": processed_job_data.get(
                    "physical_labor_intensity", ""
                ),
                "physical_position": processed_job_data.get("physical_position", ""),
                "computer_usage": processed_job_data.get("computer_usage", ""),
                "cognitive_demand": processed_job_data.get("cognitive_demand", ""),
                "oral_communication_level": processed_job_data.get(
                    "oral_communication_level", ""
                ),
                # Work Schedule
                "four_day_work_week": processed_job_data.get(
                    "four_day_work_week", False
                ),
                "overtime_required": processed_job_data.get("overtime_required", False),
                "weekend_availability_required": processed_job_data.get(
                    "weekend_availability_required", False
                ),
                "holiday_availability_required": processed_job_data.get(
                    "holiday_availability_required", False
                ),
                "morning_shift": processed_job_data.get("morning_shift_work", ""),
                "evening_shift": processed_job_data.get("evening_shift_work", ""),
                "overnight_work": processed_job_data.get("overnight_work", ""),
                "on_call_requirement": processed_job_data.get(
                    "on_call_requirement", ""
                ),
                # Benefits & Perks
                "401k_matching": processed_job_data.get("401k_matching", False),
                "retirement_plan": processed_job_data.get("retirement_plan", False),
                "generous_pto": processed_job_data.get("generous_paid_time_off", False),
                "generous_parental_leave": processed_job_data.get(
                    "generous_parental_leave", False
                ),
                "tuition_reimbursement": processed_job_data.get(
                    "tuition_reimbursement", False
                ),
                "relocation_assistance": processed_job_data.get(
                    "relocation_assistance", False
                ),
                # Special Requirements
                "language_requirements": format_array(
                    processed_job_data.get("language_requirements", [])
                ),
                "num_language_requirements": processed_job_data.get(
                    "num_language_requirements", ""
                ),
                "driver_license_required": processed_job_data.get(
                    "is_driver_license_required", False
                ),
                "security_clearance": processed_job_data.get("security_clearance", ""),
                "visa_sponsorship": processed_job_data.get("visa_sponsorship", False),
                "licenses_certifications": format_array(
                    processed_job_data.get("licenses_or_certifications", [])
                ),
                # Skills & Tools
                "technical_tools": format_array(
                    processed_job_data.get("technical_tools", [])
                ),
                "role_activities": format_array(
                    processed_job_data.get("role_activities", [])
                ),
                # Special Programs
                "fair_chance": processed_job_data.get("fair_chance", False),
                "military_veterans": processed_job_data.get("military_veterans", False),
                # Publishing Info
                "estimated_publish_date": processed_job_data.get(
                    "estimated_publish_date", ""
                ),
                "requirements_summary": processed_job_data.get(
                    "requirements_summary", ""
                ),
                # Job Description
                "description": item.get("description", ""),
                "description_snippet": (
                    item.get("description", "")[:500] + "..."
                    if item.get("description")
                    and len(item.get("description", "")) > 500
                    else item.get("description", "")
                ),
                # Engagement Metrics
                "viewed_by_users_count": len(item.get("viewedByUsers", [])),
                "hidden_from_users_count": len(item.get("hiddenFromUsers", [])),
            }

            jobs.append(job_entry)

        return jobs

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return []
    except Exception as e:
        print(f"❌ Error processing response: {e}")
        return []


def save_jobs(jobs, filename="comprehensive_jobs.csv"):
    if not jobs:
        print("❌ No jobs to save")
        return

    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"✅ Saved {len(jobs)} jobs to {filename}")

    # Print comprehensive summary
    print("\nComprehensive Job Summary:")
    print(f"Total jobs: {len(jobs)}")
    print(f"Remote jobs: {sum(1 for job in jobs if job['workplace_type'] == 'Remote')}")
    print(f"Hybrid jobs: {sum(1 for job in jobs if job['workplace_type'] == 'Hybrid')}")
    print(f"Onsite jobs: {sum(1 for job in jobs if job['workplace_type'] == 'Onsite')}")
    print(
        f"Companies: {len(set(job['company_name'] for job in jobs if job['company_name']))}"
    )
    print(
        f"Jobs with salary info: {sum(1 for job in jobs if job['is_compensation_transparent'])}"
    )
    print(
        f"Senior level positions: {sum(1 for job in jobs if 'Senior' in job['seniority_level'])}"
    )
    print(
        f"Jobs requiring travel: {sum(1 for job in jobs if job['travel_requirement_air'] not in ['', 'None', 'Not Indicated'])}"
    )


if __name__ == "__main__":
    jobs = fetch_jobs("marketing director", "New York, United States")

    if jobs:
        save_jobs(jobs, "comprehensive_jobs.csv")

        # Print detailed preview of first job
        print("Detailed preview of first job:")
        first_job = jobs[0]
        print(f"Title: {first_job['job_title']}")
        print(
            f"Company: {first_job['company_name']} ({first_job['company_employees']} employees)"
        )
        print(f"Salary: {first_job['salary_range']}")
        print(
            f"Location: {first_job['workplace_location']} ({first_job['workplace_type']})"
        )
        print(f"Experience: {first_job['min_industry_experience']} years")
        print(
            f"Education: {first_job['bachelors_required']} Bachelor's, {first_job['masters_required']} Master's"
        )
        print(f"Skills: {first_job['technical_tools']}")
        print(
            f"Travel: {first_job['travel_requirement_air']} air, {first_job['travel_requirement_land']} land"
        )
        print(
            f"Benefits: 401k: {first_job['401k_matching']}, PTO: {first_job['generous_pto']}"
        )
    else:
        print("\nNo jobs found. Try:")
        print("- Different search terms")
        print("- Different location")
        print("- Increasing date_past_days parameter")
        print("- Check if the API endpoint is still valid")
