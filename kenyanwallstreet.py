import asyncio
from playwright.async_api import async_playwright,Error
from mailer import Mail


async def newsfeed():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()

            url = 'https://kenyanwallstreet.com'

            await page.goto(url)

            await page.wait_for_load_state()
            
            container = page.locator('div.align-start a')
            
            links = await container.evaluate_all("(element) => element.map(e=>e.getAttribute('href'))")

            fullpath = []

            links_found = [ link for link in links if links ]

            for link in links_found:
                fullpath.append(f"{url}{link}")

            for path in fullpath:
                await page.goto(path)

                await page.wait_for_load_state()

                await page.wait_for_selector('h1.font-heading')

                title =await page.locator('h1.font-heading').text_content()

                await page.wait_for_selector("div.max-w-screen")

                content = await page.locator('p.text-muted-background').all_inner_texts()
                cont = [ text for text in content if text ]
                converted_text = "".join(cont)
                mail = Mail(to="grechenhanibal247@gmail.com",subject=title,content=converted_text)
                mail.sendmail()
                await asyncio.sleep(5)

    except Error as e:
        print(f"Playwright Error:{e}")

asyncio.run(newsfeed())
