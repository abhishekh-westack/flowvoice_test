import pytest
import allure
import os
import time
from pathlib import Path
from core.playwright.browser import browser
from core.utils.gcs_uploader import get_gcs_uploader
from config.env import DELETE_LOCAL_AFTER_GCS_UPLOAD

# Import page fixtures
from fixtures.page_fixtures import login_page, otp_page, login_flow

@pytest.fixture
def context(browser, request):

    video_dir = Path("videos").absolute()
    video_dir.mkdir(exist_ok=True)


    existing_videos = set(video_dir.glob("*.webm"))

    ctx = browser.new_context(
        record_video_dir=str(video_dir),
        record_video_size={"width": 1280, "height": 720},
    )

    yield ctx

    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    ctx.close()

    all_videos = set(video_dir.glob("*.webm"))
    new_videos = all_videos - existing_videos
    
    # Get GCS uploader
    gcs = get_gcs_uploader()

    for video_path in new_videos:
        if not video_path.exists() or os.path.getsize(video_path) == 0:
            print(f"⚠ Skipping empty video: {video_path}")
            continue

        if test_failed:
            try:
                # Upload to GCS first
                video_url = gcs.upload_video(str(video_path), request.node.name)
                
                if video_url and gcs.enabled:
                    # Attach GCS URL as link instead of embedding video
                    allure.attach(
                        video_url,
                        name="Video (GCS)",
                        attachment_type=allure.attachment_type.URI_LIST,
                    )
                    print(f"✓ Video URL attached to Allure: {video_url}")
                    
                    # Delete local file after successful upload (if configured)
                    if DELETE_LOCAL_AFTER_GCS_UPLOAD:
                        try:
                            os.remove(video_path)
                            print(f"✓ Deleted local video (uploaded to GCS)")
                        except Exception as del_error:
                            print(f"⚠ Could not delete local video: {del_error}")
                else:
                    # Fallback: embed video if GCS upload failed
                    with open(video_path, "rb") as vf:
                        allure.attach(
                            vf.read(),
                            name=f"{request.node.name}_video",
                            attachment_type=allure.attachment_type.WEBM,
                        )
                    print(f"✓ Video embedded in Allure: {video_path} ({os.path.getsize(video_path)} bytes)")
                    
            except Exception as e:
                print(f"✗ Failed to process video: {e}")
        else:
            try:
                os.remove(video_path)
                print(f"✓ Deleted video: {video_path}")
            except Exception as e:
                print(f"✗ Failed to delete video: {e}")

@pytest.fixture
def page(context, request):
    page = context.new_page()
    yield page

    # --- Screenshot logic commented out ---
    # test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    # 
    # # Get GCS uploader
    # gcs = get_gcs_uploader()
    #
    # if test_failed:
    #     screenshot_dir = Path("screenshots/failures")
    #     screenshot_dir.mkdir(parents=True, exist_ok=True)
    #
    #     screenshot_path = screenshot_dir / f"{request.node.name}.png"
    #
    #     screenshot_bytes = page.screenshot(path=str(screenshot_path))
    #
    #     # Upload to GCS first
    #     screenshot_url = gcs.upload_screenshot(str(screenshot_path), request.node.name)
    #     
    #     if screenshot_url and gcs.enabled:
    #         # Attach GCS URL as link instead of embedding image
    #         allure.attach(
    #             screenshot_url,
    #             name="Screenshot (GCS)",
    #             attachment_type=allure.attachment_type.URI_LIST,
    #         )
    #         print(f"✓ Screenshot URL attached to Allure: {screenshot_url}")
    #         
    #         # Delete local file after successful upload (if configured)
    #         if DELETE_LOCAL_AFTER_GCS_UPLOAD:
    #             try:
    #                 os.remove(screenshot_path)
    #                 print(f"✓ Deleted local screenshot (uploaded to GCS)")
    #             except Exception as del_error:
    #                 print(f"⚠ Could not delete local screenshot: {del_error}")
    #     else:
    #         # Fallback: embed screenshot if GCS upload failed
    #         allure.attach(
    #             screenshot_bytes,
    #             name=f"{request.node.name}_screenshot",
    #             attachment_type=allure.attachment_type.PNG,
    #         )
    #         print(f"✓ Screenshot embedded in Allure: {screenshot_path}")
    # --- End screenshot logic ---
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


__all__ = ["browser", "context", "page"]
