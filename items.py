# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class KickItem(scrapy.Item):
    project_name = scrapy.Field()
    project_description = scrapy.Field()
    creator = scrapy.Field()
    pledged = scrapy.Field()
    goal = scrapy.Field()
    backers_count = scrapy.Field()
    creator_url = scrapy.Field()
    image = scrapy.Field()
    video = scrapy.Field()
    project_location = scrapy.Field()
    subcategory = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    project_status = scrapy.Field()

    creator_location = scrapy.Field()
    creator_description = scrapy.Field()
    creator_realname = scrapy.Field()
    creator_lastlogin = scrapy.Field()
    creator_facebook = scrapy.Field()
    creator_created_count = scrapy.Field()
    creator_backed_count  = scrapy.Field()
    creator_website = scrapy.Field()
    creator_id = scrapy.Field()

    faq_url= scrapy.Field()
    updates_url = scrapy.Field()
    comments_url = scrapy.Field()
    community_url = scrapy.Field()

    #faq
    faq_count = scrapy.Field()
    faq_question = scrapy.Field()
    faq_answer = scrapy.Field()

    #updates
    updates_count = scrapy.Field()
    updates_content = scrapy.Field()
    updates_title = scrapy.Field()
    updates_date = scrapy.Field()
    updates_creator = scrapy.Field()
    updates_heart = scrapy.Field()
    updates_comments = scrapy.Field()

    #comments
    comments_count = scrapy.Field()
    comments_content = scrapy.Field()
    comments_name = scrapy.Field()
    comments_date = scrapy.Field()

    #community
    community_topcity_city = scrapy.Field()
    community_topcity_country = scrapy.Field()
    community_topcity = scrapy.Field()
    community_topcity_backers = scrapy.Field()
    community_topcountry = scrapy.Field()
    community_topcountry_country = scrapy.Field()
    community_topcountry_backers = scrapy.Field()

    newbacker = scrapy.Field()
    oldbacker = scrapy.Field()

    # pledge
    pledge_money = scrapy.Field()
    pledge_name = scrapy.Field()
    pledge_description = scrapy.Field()
    pledge_includes = scrapy.Field()
    pledge_delivery = scrapy.Field()
    pledge_backer = scrapy.Field()
    pledge_ship = scrapy.Field()

    state = scrapy.Field()
    id = scrapy.Field()
    json_url = scrapy.Field()
    link = scrapy.Field()
    daystogo = scrapy.Field()

    story = scrapy.Field()
    risks = scrapy.Field()
    environmental_commitments = scrapy.Field()
    budget_category = scrapy.Field()
    budget_sub_category = scrapy.Field()
    budget_category_cost = scrapy.Field()
    budget_sub_category_cost = scrapy.Field()

