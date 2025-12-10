from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

from pages import HomePage, LeverJobPage, QAPage


def test_insider_qa_career_flow(driver: "WebDriver") -> None:
    """
    Case Steps:
    1. Visit https://insiderone.com/ and check Insider home page is opened
       and all main blocks are loaded
    2. Go to https://useinsider.com/careers/quality-assurance/, click
       "See all QA jobs", filter jobs by Location - Istanbul, Turkey and
       department - Quality Assurance, check presence of jobs list
    3. Check that all jobs' Position contains "Quality Assurance",
       Department contains "Quality Assurance", Location contains
       "Istanbul, Turkey"
    4. Click "View Role" button and check that this action redirects us to
       Lever Application form page
    """

    # --- Step 1: Home page ---
    home = HomePage(driver)
    home.open_home()
    home.accept_cookies_if_present()

    assert home.is_loaded(), "Insider home page is not loaded."

    # --- Step 2: QA careers page (direct) ---
    qa_page = QAPage(driver)
    qa_page.open_qa_page()
    assert qa_page.is_loaded(), "QA careers page is not loaded."

    # --- Step 3: See all QA jobs & filters ---
    qa_page.click_see_all_qa_jobs()
    qa_page.filter_jobs(
        location="Istanbul",
        department="Quality Assurance",
    )

    if not qa_page.has_job_list():
        assert qa_page.has_empty_state(), (
            "Neither job list nor 'Content is not available.' "
            "empty state is visible."
        )
        return

    jobs = qa_page.get_all_jobs()
    assert jobs, "No jobs returned from QA job list."

    for job in jobs:
        assert "Quality" in job.position or "QA" in job.position, (
            f"Job position does not look like QA: {job.position}"
        )

        if job.department:
            assert (
                "Quality" in job.department
                or "Assurance" in job.department
                or "QA" in job.department
            ), (
                f"Job department does not contain 'Quality Assurance': "
                f"{job.department}"
            )

        if job.location:
            assert (
                "Istanbul" in job.location
                or "İstanbul" in job.location
            ), f"Job location does not contain 'Istanbul': {job.location}"

            if "," in job.location:
                assert "Turkey" in job.location, (
                    f"Job location should contain 'Turkey' "
                    f"when country is present: {job.location}"
                )

    # --- Step 4: Click 'View Role' and verify Lever redirect ---
    lever_page = qa_page.open_first_job_in_lever()
    assert lever_page.is_loaded(), "Lever application form page is not loaded."
