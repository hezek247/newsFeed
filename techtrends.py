from playwright.async_api import async_playwright
import asyncio
from datetime import datetime,timedelta,date
from mailer import Mail


url = "https://techtrendske.co.ke/"
now = datetime.now()
now = now.strftime("%B %d %Y")
con_now = datetime.strptime(now,'%B %d %Y')
duration_now = con_now - timedelta(days=7)


async def tech_trends():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url)
        await page.wait_for_load_state()

        await page.locator("div#tnp-modal-close").click()
        await page.locator('nav#top-nav li#menu-item-52841 a').click()
        await page.wait_for_selector('div.main-content')
        news = []

        boxes = page.locator('li.post-item')
        count = await boxes.count()
        length = range(count)

        for i in length:
            box = boxes.nth(i)

            link = box.locator('h2 a')
            day = await box.locator('span.date').inner_text()
            link_address = await link.get_attribute('href')
            link_text = await link.inner_text()

            con_day = datetime.strptime(day,'%B %d, %Y').date().strftime('%B %d %Y')
            usable_day = datetime.strptime(con_day,'%B %d %Y')

            if usable_day >= duration_now:
                page_details = {
                        'title': link_text.strip(),
                        'anchor': link_address,
                        'publication': usable_day
                    }

                news.append(page_details)
                if news[-1]['publication'] >= duration_now:
                    await page.locator('a.next-posts').click()

        return news


if __name__ == "__main__":
   content = asyncio.run(tech_trends())
   for i in range(len(content)):
       title = content[i]['title']
       body = content[i]['anchor']
       mail = Mail(to="grechenhanibal247@gmail.com", subject =title, content=body)
       mail.sendmail()