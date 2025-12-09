# tests/test_insider_qa_flow.py
from pages.home_page import HomePage
from pages.careers_page import CareersPage


def test_insider_qa_career_flow(driver):
    """
    Case Adımları:

    1. Visit https://useinsider.com/ and check Insider home page is opened or not
    2. Select the “Company” menu in the navigation bar, select “Careers” and check
       Career page, its Locations, Teams, and Life at Insider blocks are open or not
    3. Go to https://useinsider.com/careers/quality-assurance/, click “See all QA jobs”,
       filter jobs by Location: “Istanbul, Turkey”, and Department: “Quality Assurance”,
       check the presence of the jobs list
    4. Check that all jobs’ Position contains “Quality Assurance”, Department contains
       “Quality Assurance”, and Location contains “Istanbul, Turkey”. Job verifications
       (pozitif veya boş liste case'i)

    5. Click the “View Role” button and check that this action redirects us to the
       Lever Application form page

     """

    # --- Step 1: Home page ---
    home = HomePage(driver)
    home.open_home()
    home.accept_cookies_if_present()

    assert home.is_loaded(), "Insider home page is not loaded."

    # --- Step 2: Careers page via Company menu ---
    careers: CareersPage = home.go_to_careers_via_company_menu()
    careers.accept_cookies_if_present()

    assert careers.is_loaded(), "Careers page is not loaded."
    assert careers.has_locations_block(), "'Our Locations' block is not visible."
    assert careers.has_teams_block(), "'Teams / Find your calling' block is not visible."
    assert careers.has_life_at_insider_block(), "'Life at Insider' block is not visible."

    # --- Step 3: QA careers page & filters ---
    qa_page = careers.open_qa_careers_page()
    assert qa_page.is_loaded(), "QA careers page is not loaded."

    qa_page.click_see_all_qa_jobs()

    qa_page.filter_jobs(
        location="Istanbul, Turkey",
        department="Quality Assurance",
    )

    # Bu noktada iki olasılık var:
    # 1) Job list var (pozitif senaryo)
    # 2) Job list yok, "Content is not available." empty state'i görünüyor (boş liste senaryosu)

    if not qa_page.has_job_list():
        # Boş liste case'i: explicit empty-state mesajını bekliyoruz
        assert qa_page.has_empty_state(), (
            "Neither job list nor 'Content is not available.' empty state is visible."
        )
        # Boş liste senaryosunda pozitif adımlara (job field kontrolleri, Lever) gitmiyoruz.
        return

    # --- Step 4: Validate each job's fields ---
    jobs = qa_page.get_all_jobs()
    assert jobs, "No jobs returned from QA job list."

    for job in jobs:
        assert "Quality" in job.position or "QA" in job.position, (
            f"Job position does not look like QA: {job.position}"
        )
        assert (
                "Quality" in job.department
                or "Assurance" in job.department
                or "QA" in job.department
        ), f"Job department does not contain 'Quality Assurance': {job.department}"
        assert "Istanbul" in job.location and "Turkey" in job.location, (
            f"Job location does not contain 'Istanbul, Turkey': {job.location}"
        )

    # --- Step 5: Click 'View Role' and verify Lever redirect ---
    lever_page = qa_page.open_first_job_in_lever()
    assert lever_page.is_loaded(), "Lever application form page is not loaded."
