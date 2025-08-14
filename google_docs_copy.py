import time
import pyperclip
from playwright.sync_api import sync_playwright, Playwright, TimeoutError as PlaywrightTimeoutError

def copy_google_doc_content(playwright: Playwright):
    document_url = "https://docs.google.com/document/d/10whwZzYqdhE0hJadehajaJGypAdr0ulKG0Pzm7FPuC0/edit?usp=sharing"

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    # ----------------

    browser = playwright.chromium.launch(
        executable_path=chrome_path,
        headless=True
    )
    context = browser.new_context(
        locale="ja-JP",
    )
    page = context.new_page()

    try:
        print(f"Googleドキュメントにアクセスしています: {document_url}")
        page.goto(document_url, wait_until="load", timeout=60000)

        print("ドキュメントの読み込みを待っています...")
        editor_selector = 'div.kix-page-paginated'
        page.wait_for_selector(editor_selector, timeout=60000)
        print("ドキュメントの読み込みが完了しました。")

        page.locator(editor_selector).first.click()
        time.sleep(1)

        print("すべてのコンテンツを選択しています (Ctrl+A)...")
        page.keyboard.press("Control+A")
        time.sleep(1)  # 選択が反映されるのを待機

        print("選択範囲のテキストを取得しています...")
        selected_text = page.evaluate("() => window.getSelection().toString()")

        if selected_text:
            print("クリップボードにテキストをコピーしています...")
            pyperclip.copy(selected_text)

            # 完了メッセージを表示
            print("\n--------------------")
            print("コピーしました")
            print("--------------------")
            time.sleep(2)  # 2秒間待機
        else:
            print("エラー: テキストの取得に失敗しました。ドキュメントが空か、選択がうまくいかなかった可能性があります。")

    except PlaywrightTimeoutError:
        print(f"エラー: タイムアウトしました。ページの読み込みに失敗したか、指定された要素 '{editor_selector}' が見つかりませんでした。")
        print("ネットワーク接続を確認するか、セレクタが正しいか確認してください。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
    finally:
        print("ブラウザを閉じています。")
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        copy_google_doc_content(playwright)
