import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict
import spacy

qa_pairs = [
    {
        "question": "What makes Jessup Cellars' atmosphere unique?",
        "answer": "Jessup Cellars has a casual and inviting atmosphere and was the first tasting room opened in Yountville in 2003. You have the option of sitting inside our stunning art gallery or you may choose to enjoy the patio with giant umbrellas. We also have space available for private groups and special accommodations and snacks for your children. Our fine art is meticulously curated by our lead artist Jermaine Dante who exhibits his colorful creations in large formats in our spacious gallery where you can take in, or take home the inspiring art while imbibing your favorite Jessup wines."
    },
    {
        "question": "Who founded Jessup Cellars and what is their mission?",
        "answer": "Jessup Cellars was founded by Dan and Becky Blue, Roy and Cheri Eisiminger, Vance and Jana Thompson, Jim and Kelly Mazzo, Kerry and Cindi Solomon, and Eric and Marleen Donnenfeld. Their mission is to create and share life-enriching experiences for their members and guests, while also giving back to the community through the support of the arts."
    },
    {
        "question": "What special events does Jessup Cellars host?",
        "answer": "Jessup Cellars hosts a variety of special events including its Art House Sessions summer music series and Art House Short Film Series. They also offer sit-down, hosted tastings in the winery’s spacious gallery among curated art, which features rotating installations by celebrated regional and national artists."
    },
    {
        "question": "Why is Jessup Cellars wine club membership unique?",
        "answer": "Jessup Cellars wine club membership offers exclusive access to limited release wines and member-only events. It is considered one of the best experiences in wine in the Napa Valley, allowing members to share great wine and food with friends and family, both locally and when traveling home."
    },
    {
        "question": "What makes Jessup Cellars unique compared to other tasting rooms in Yountville?",
        "answer": "Jessup Cellars has a casual and inviting atmosphere and was the first tasting room opened in Yountville in 2003. You have the option of sitting inside our stunning art gallery or you may choose to enjoy the patio with giant umbrellas. We also have space available for private groups and special accomodations and snacks for your children. Our fine art is meticulously curated by our lead artist Jermaine Dante who exhibits his colorful creations in large formats in our spacious gallery where you can take in, or take home the inspiring art while imbibing your favorite Jessup wines."
    },
    {
        "question": "Who is the resident artist at Jessup Cellars?",
        "answer": "Jermaine Danté is the resident artist at Jessup Cellars. His artwork is characterized by bold strokes and evocative imagery, often capturing the essence of Wine Country."
    },
    {
        "question": "What is unique about Jermaine Danté's artwork at Jessup Cellars?",
        "answer": "Jermaine Danté's artwork at Jessup Cellars embodies the symbiotic relationship between art and wine. As a certified sommelier, he infuses his pieces with a unique perspective on Wine Country."
    },
    {
        "question": "Where is Jessup Cellars located?",
        "answer": "Jessup Cellars and Tasting Gallery is located at 6740 Washington St. at the North end of Yountville, across from RH Yountville and North Block Restaurant."
    },
    {
        "question": "What are the operating hours of Jessup Cellars?",
        "answer": "Jessup Cellars is open from 10AM to 5:30PM, seven days a week."
    },
    {
        "question": "How can you contact Jessup Cellars for reservations and information?",
        "answer": "You can reach Jessup Cellars at 707.944.5620 for reservations and information."
    },
    {
        "question": "Is Jessup Cellars pet-friendly?",
        "answer": "Yes, Jessup Cellars welcomes well-behaved dogs inside or outside. They provide gluten-free dog treats and water dishes."
    },
    {
        "question": "Who is the consulting winemaker for Jessup Cellars?",
        "answer": "Rob Lloyd is the consulting winemaker for Jessup Cellars. He is renowned for crafting Chardonnay for Rombauer, La Crema, and Cakebread."
    },
    {
        "question": "What awards has Jessup Cellars won?",
        "answer": "Jessup Cellars has won numerous awards, including CellarPass’ ‘Friendliest & Most Knowledgeable Staff’ three years in a row, Napa Valley Life magazine’s ‘Best Wine Club’, and Yountville’s ‘Business of the Year’."
    },
    {
        "question": "What is Rob Lloyd's background in winemaking?",
        "answer": "Rob Lloyd started his career in wine after college, working at various prestigious wineries including Cakebread, Stag’s Leap Wine Cellars, and La Crema. He earned his MS in Viticulture & Enology from UC Davis."
    },
    {
        "question": "What is Bernardo Munoz's role at Jessup Cellars?",
        "answer": "Bernardo Munoz is a winemaker at Jessup Cellars. He started in the vineyards and brings his grape-to-bottle knowledge to the team."
    },
    {
        "question": "What is the leading white wine at Jessup Cellars?",
        "answer": "The leading white wine at Jessup Cellars is the Napa Valley Chardonnay from the Los Carneros region."
    },
    {
        "question": "Where are the grapes for Jessup Cellars' Napa Valley Chardonnay sourced from?",
        "answer": "The grapes for Jessup Cellars' Napa Valley Chardonnay are sourced from the Truchard Vineyard, located in the hills above Highway 12 with San Francisco Bay influences."
    },
    {
        "question": "What is unique about the climate and terroir of the Truchard Vineyard?",
        "answer": "The cooler growing climate and ideal terroir of the Truchard Vineyard allow the grapes to ripen slowly and perfectly on the vine, creating a well-balanced Chardonnay."
    },
    {
        "question": "How is Jessup Cellars' Napa Valley Chardonnay aged?",
        "answer": "Jessup Cellars' Napa Valley Chardonnay is aged for 10 months in 40% new American Oak barrels, which adds hints of oak to the wine and a slightly creamy mouthfeel."
    },
    {
        "question": "What is the alcohol content and PH of Jessup Cellars' Napa Valley Chardonnay?",
        "answer": "The alcohol content of Jessup Cellars' Napa Valley Chardonnay is 14.8%, and the PH is 3.4."
    },
    {
        "question": "What is the price of Jessup Cellars' Napa Valley Chardonnay for non-members?",
        "answer": "The non-member price for Jessup Cellars' Napa Valley Chardonnay is $55."
    },
    {
        "question": "Where is Jessup Cellars' Sauvignon Blanc sourced from?",
        "answer": "Jessup Cellars' Sauvignon Blanc is sourced from North Coast vineyards outside of the Napa Valley."
    },
    {
        "question": "What makes Jessup Cellars' 2023 Sauvignon Blanc different from typical Sauvignon Blanc?",
        "answer": "Jessup Cellars' 2023 Sauvignon Blanc has a tropical nature that is different from the typical Sauvignon Blanc grown in the Valley and elsewhere in the World."
    },
    {
        "question": "How is Jessup Cellars' 2023 Sauvignon Blanc aged?",
        "answer": "Jessup Cellars' 2023 Sauvignon Blanc is aged in 100% stainless steel barrels, which seals out the oxygen and seals in the flavors of the fruit."
    },
    {
        "question": "What is the alcohol content and PH of Jessup Cellars' 2023 Sauvignon Blanc?",
        "answer": "The alcohol content of Jessup Cellars' 2023 Sauvignon Blanc is 15.1%, and the PH is 3.3."
    },
    {
        "question": "What are the flavor notes of Jessup Cellars' 2023 Sauvignon Blanc?",
        "answer": "Jessup Cellars' 2023 Sauvignon Blanc has hints of pineapple and mango, with a balanced fruit flavor that is not too fruit forward."
    },
    {
        "question": "What is the non-member price of Jessup Cellars' 2023 Sauvignon Blanc?",
        "answer": "The non-member price of Jessup Cellars' 2023 Sauvignon Blanc is $45."
    },
    {
        "question": "What dishes pair well with Jessup Cellars' 2023 Sauvignon Blanc?",
        "answer": "Jessup Cellars' 2023 Sauvignon Blanc pairs well with dishes like Grilled Prawn Cocktail, Ceviche, Tacos, and Peach & Burrata salad."
    },
    {
        "question": "What is the mouthfeel of Jessup Cellars' Napa Valley Chardonnay?",
        "answer": "The Napa Valley Chardonnay from Jessup Cellars has a slightly creamy mouthfeel without being overly buttery."
    },
    {
        "question": "Who crafted the Jessup Cellars Napa Valley Chardonnay?",
        "answer": "The Jessup Cellars Napa Valley Chardonnay is crafted by renowned consulting winemaker Rob Lloyd."
    },
    {
        "question": "Why is Jessup Cellars' Sauvignon Blanc considered a 'hot tub wine'?",
        "answer": "Jessup Cellars' Sauvignon Blanc is considered a 'hot tub wine' because of its refreshing qualities, making it perfect for warm summer evenings after a long day in the sun."
    },
    {
        "question": "What types of red wines does Jessup Cellars offer?",
        "answer": "Jessup Cellars offers a range of red wines including Pinot Noir, Merlot blends, blended Cabernet Sauvignon, Mendocino Rougette, 100% Zinfandel, 100% Petite Sirah, and seasonal favorites like Manny's Blend."
    },
    {
        "question": "What makes Jessup Cellars' Pinot Noir unique?",
        "answer": "Jessup Cellars' Pinot Noir is unique due to the 'Art of the Blend'. While it is 96.7% Pinot Noir from the Los Carneros Truchard Vineyard, it is blended with 3.3% Petite Sirah from the Wooden Valley area, aged in 50% new French oak for 10 months, giving it a bolder color and added body."
    },
    {
        "question": "What is the alcohol content and PH of Jessup Cellars' 2021 Pinot Noir?",
        "answer": "The alcohol content of Jessup Cellars' 2021 Pinot Noir is 14.8%, and the PH is 3.45."
    },
    {
        "question": "What is the non-member price of Jessup Cellars' 2021 Pinot Noir?",
        "answer": "The non-member price of Jessup Cellars' 2021 Pinot Noir is $70."
    },
    {
        "question": "What are the varietals in Jessup Cellars' 2019 Rougette?",
        "answer": "Jessup Cellars' 2019 Rougette is a blend of 87% Grenache and 13% Carignane, sourced from the Mendocino growing region."
    },
    {
        "question": "How is Jessup Cellars' 2019 Rougette aged?",
        "answer": "Jessup Cellars' 2019 Rougette is aged by co-fermenting the varietals for 15 months in used (neutral) Chardonnay barrels."
    },
    {
        "question": "What is the flavor profile of Jessup Cellars' 2019 Rougette?",
        "answer": "The 2019 Rougette has aromas of sweet strawberry, ripe cranberry jam, red plum, cassis, and nutmeg, with a dry palate, fresh acidity, and silky, rich tannins."
    },
    {
        "question": "What dishes pair well with Jessup Cellars' 2019 Rougette?",
        "answer": "Jessup Cellars' 2019 Rougette pairs well with duck confit, mushroom risotto, or an assortment of softer cheeses."
    },
    {
        "question": "What makes Jessup Cellars' 2020 Pacini Vineyards 100% Zinfandel unique?",
        "answer": "Jessup Cellars' 2020 Pacini Vineyards 100% Zinfandel is unique due to its grapes coming from 134-year-old 'ancient vines' in the Talmage Bench in Mendocino County."
    },
    {
        "question": "What is the flavor profile of Jessup Cellars' 2020 Pacini Vineyards Zinfandel?",
        "answer": "The 2020 Pacini Vineyards Zinfandel has nuances of ripe cranberry, pomegranate, cherry cola, white pepper, and vanilla, with soft tannins and a long finish."
    },
    {
        "question": "What is the alcohol content and PH of Jessup Cellars' 2020 Pacini Vineyards Zinfandel?",
        "answer": "The alcohol content of Jessup Cellars' 2020 Pacini Vineyards Zinfandel is 14.9%, and the PH is 3.35."
    },
    {
        "question": "What is the non-member price of Jessup Cellars' 2020 Pacini Vineyards Zinfandel?",
        "answer": "The non-member price of Jessup Cellars' 2020 Pacini Vineyards Zinfandel is $60."
    },
    {
        "question": "What dishes pair well with Jessup Cellars' 2020 Pacini Vineyards Zinfandel?",
        "answer": "Jessup Cellars' 2020 Pacini Vineyards Zinfandel pairs well with pastas, barbecued meats, or enjoyed on its own."
    },
    {
        "question": "Where is Jessup Cellars' 2019 Merlot sourced from?",
        "answer": "Jessup Cellars' 2019 Merlot is sourced from the Truchard Vineyard in the Los Carneros region of the Napa Valley."
    },
    {
        "question": "What is the blend composition of Jessup Cellars' 2019 Merlot?",
        "answer": "Jessup Cellars' 2019 Merlot is 80% Merlot, 16.5% Cabernet Sauvignon from the Chiles Valley AVA, and 3.5% Petite Sirah from the same location."
    },
    {
        "question": "How is Jessup Cellars' 2019 Merlot aged?",
        "answer": "Jessup Cellars' 2019 Merlot is aged for 22 months in 40% new American/French oak."
    },
    {
        "question": "What is the alcohol content and PH of Jessup Cellars' 2019 Merlot?",
        "answer": "The alcohol content of Jessup Cellars' 2019 Merlot is 15.1%, and the PH is 3.55."
    },
    {
        "question": "What dishes pair well with Jessup Cellars' 2019 Merlot?",
        "answer": "Jessup Cellars' 2019 Merlot pairs well with roasted chicken and vegetables or beef bourguignon."
    },
    {
        "question": "What is the non-member price of Jessup Cellars' 2019 Merlot?",
        "answer": "The non-member price of Jessup Cellars' 2019 Merlot is $70."
    },
    {
        "question": "What is the blend composition of Jessup Cellars' 2019 Napa Valley Cabernet Sauvignon?",
        "answer": "Jessup Cellars' 2019 Napa Valley Cabernet Sauvignon is 90% Napa Valley fruit from the Chiles Valley AVA, 5% Petite Sirah, 3% Merlot, and 2.1% Cabernet Franc."
    },
    {
        "question": "How is Jessup Cellars' 2019 Napa Valley Cabernet Sauvignon aged?",
        "answer": "Jessup Cellars' 2019 Napa Valley Cabernet Sauvignon is aged in 80% new French oak for 22 months."
    },
    {
        "question": "What is the alcohol content and PH of Jessup Cellars' 2019 Napa Valley Cabernet Sauvignon?",
        "answer": "The alcohol content of Jessup Cellars' 2019 Napa Valley Cabernet Sauvignon is 14.9%, and the PH is 3.65."
    },
    {
        "question": "What is the non-member price of Jessup Cellars' 2019 Napa Valley Cabernet Sauvignon?",
        "answer": "The non-member price of Jessup Cellars' 2019 Napa Valley Cabernet Sauvignon is $90."
    },
    {
        "question": "What dishes pair well with Jessup Cellars' 2019 Napa Valley Cabernet Sauvignon?",
        "answer": "Jessup Cellars' 2019 Napa Valley Cabernet Sauvignon pairs well with a quality cut of beef or any dish with a smoky, fatty, or charred quality."
    },
    {
        "question": "What is the blend composition of Jessup Cellars' 2018 Alexander Valley Cabernet Sauvignon?",
        "answer": "Jessup Cellars' 2018 Alexander Valley Cabernet Sauvignon is 96.5% Cabernet grapes, finished with 3.5% Napa Valley Petite Sirah."
    },
    {
        "question": "How is Jessup Cellars' 2018 Alexander Valley Cabernet Sauvignon aged?",
        "answer": "Jessup Cellars' 2018 Alexander Valley Cabernet Sauvignon is aged in 80% new French oak."
    },
    {
        "question": "What is the alcohol content of Jessup Cellars' 2018 Alexander Valley Cabernet Sauvignon?",
        "answer": "The alcohol content of Jessup Cellars' 2018 Alexander Valley Cabernet Sauvignon is 14.9%."
    },
    {
        "question": "What dishes pair well with Jessup Cellars' 2018 Alexander Valley Cabernet Sauvignon?",
        "answer": "Jessup Cellars' 2018 Alexander Valley Cabernet Sauvignon pairs well with Filet Mignon or other red meats."
    },
    {
        "question": "What makes Jessup Cellars' 'Graziella' blend unique?",
        "answer": "'Graziella' is unique due to its harmonious blend of Sangiovese and Cabernet Sauvignon, its limited production, and the special balance of aromas and flavors such as strawberry, red plum, raspberry, vanilla, and rose petal."
    },
    {
        "question": "What is the price of Jessup Cellars' 'Graziella' blend?",
        "answer": "The price of Jessup Cellars' 'Graziella' blend is $95."
    },
    {
        "question": "What dishes pair well with Jessup Cellars' 'Graziella' blend?",
        "answer": "Jessup Cellars' 'Graziella' blend pairs well with red sauce dishes like lasagna or spiced meat dishes like lamb with rosemary."
    },
    {
        "question": "What is the composition of Jessup Cellars' 'Graziella' blend?",
        "answer": "Jessup Cellars' 'Graziella' blend is composed of 75% Sangiovese and 25% Cabernet Sauvignon."
    },
    {
        "question": "How long is Jessup Cellars' 'Graziella' blend aged?",
        "answer": "Jessup Cellars' 'Graziella' blend is aged for 15 months in French oak."
    },
    {
        "question": "What is the alcohol content and PH of Jessup Cellars' 'Graziella' blend?",
        "answer": "The alcohol content of Jessup Cellars' 'Graziella' blend is 14.9%, and the PH is 3.6."
    },
    {
        "question": "What is the composition of Jessup Cellars' 2019 'Juel' Red Wine?",
        "answer": "Jessup Cellars' 2019 'Juel' Red Wine is composed of 56% Napa Valley Cabernet Sauvignon, 14% Cabernet Franc, 24% Merlot, 2% Petite Sirah, 2% Petite Verdot, and 2% Malbec."
    },
    {
        "question": "How long is Jessup Cellars' 2019 'Juel' Red Wine aged?",
        "answer": "Jessup Cellars' 2019 'Juel' Red Wine is aged for 22 months in 70% new French oak."
    },
    {
        "question": "What is the alcohol content and PH of Jessup Cellars' 2019 'Juel' Red Wine?",
        "answer": "The alcohol content of Jessup Cellars' 2019 'Juel' Red Wine is 14.9%, and the PH is 3.65."
    },
    {
        "question": "What is the non-member price of Jessup Cellars' 2019 'Juel' Red Wine?",
        "answer": "The non-member price of Jessup Cellars' 2019 'Juel' Red Wine is $115."
    },
    {
        "question": "What is the composition of Jessup Cellars' 2019 'Table for Four' Cabernet Blend?",
        "answer": "Jessup Cellars' 2019 'Table for Four' Cabernet Blend is composed of 61.8% Cabernet Sauvignon, 26.5% Cabernet Franc, 4.2% Petite Verdot, 3.5% Petite Sirah, 2.7% Malbec, and 1.1% Merlot."
    },
    {
        "question": "How long is Jessup Cellars' 2019 'Table for Four' Cabernet Blend aged?",
        "answer": "Jessup Cellars' 2019 'Table for Four' Cabernet Blend is aged for 22 months in 70% new French oak."
    },
    {
        "question": "What is the alcohol content and PH of Jessup Cellars' 2019 'Table for Four' Cabernet Blend?",
        "answer": "The alcohol content of Jessup Cellars' 2019 'Table for Four' Cabernet Blend is 14.9%, and the PH is 3.65."
    },
    {
        "question": "What is the non-member price of Jessup Cellars' 2019 'Table for Four' Cabernet Blend?",
        "answer": "The non-member price of Jessup Cellars' 2019 'Table for Four' Cabernet Blend is $115."
    },
    {
        "question": "What is unique about Jessup Cellars' 2021 Petite Sirah?",
        "answer": "Jessup Cellars' 2021 Petite Sirah is unique due to its complex blend of flavors and aromas, including notes of blueberry, tart cherry, pomegranate, brown sugar, cassis, bourbon, sour mash, plum jam, cracked pepper, cedar, licorice, and raspberry. It also has robust yet approachable tannins and bright acidity."
    },
    {
        "question": "How long is Jessup Cellars' 2021 Petite Sirah aged?",
        "answer": "Jessup Cellars' 2021 Petite Sirah is aged for 22 months in a mix of used (neutral) French and American barrels."
    },
    {
        "question": "What is the alcohol content and PH of Jessup Cellars' 2021 Petite Sirah?",
        "answer": "The alcohol content of Jessup Cellars' 2021 Petite Sirah is 15.6%, and the PH is 3.65."
    },
    {
        "question": "What fortified wines does Jessup Cellars offer?",
        "answer": "Jessup Cellars offers Zinfandel Port and a 100% Cabernet Sauvignon dessert wine."
    },
    {
        "question": "What is unique about Jessup Cellars' 2013 Zinfandel Port?",
        "answer": "Jessup Cellars' 2013 Zinfandel Port is fortified with brandy and boasts bold aromatics of ripe raspberry, leather, and spice on the nose, followed by vanilla and red plum on the palate. It has an alcohol content of 19.5%."
    },
    {
        "question": "How should Jessup Cellars' 2013 Zinfandel Port be enjoyed?",
        "answer": "Jessup Cellars' 2013 Zinfandel Port pairs well with blue cheese, dark chocolate, or a Maduro cigar. It can be enjoyed now or cellared for 7-10 years."
    },
    {
        "question": "What is the price of Jessup Cellars' 2013 Zinfandel Port for non-members?",
        "answer": "The price of Jessup Cellars' 2013 Zinfandel Port for non-members is $65."
    },
    {
        "question": "What aromas and flavors are present in Jessup Cellars' 13th Reflection Tawny dessert wine?",
        "answer": "Jessup Cellars' 13th Reflection Tawny dessert wine offers aromas of stewed cherry, dried fig, chocolate, and baking spice with a kiss of sandalwood and cedar. The palate features mixed berry preserves."
    },
    {
        "question": "How should Jessup Cellars' 13th Reflection Tawny dessert wine be enjoyed?",
        "answer": "Jessup Cellars' 13th Reflection Tawny dessert wine pairs well with chocolate lava cake or a cheese course of ripe, aged, salty cheeses. It can be enjoyed now or cellared for 10-15 years."
    },
    {
        "question": "What is the composition and aging process of Jessup Cellars' Infinite Reflection 13th Recursion?",
        "answer": "The Infinite Reflection 13th Recursion is 100% Napa Valley Cabernet Sauvignon aged for 12 years in French oak with an alcohol content of 19.5%."
    },
    {
        "question": "What is the price of Jessup Cellars' Infinite Reflection 13th Recursion for non-members?",
        "answer": "The price of Jessup Cellars' Infinite Reflection 13th Recursion for non-members is $85."
    },
    {
        "question": "What is the Solera method used in Jessup Cellars' dessert wine production?",
        "answer": "The Solera method is a traditional aging and blending process that involves a series of barrels arranged in a tiered system. Older wines in the bottom row are partially emptied and topped up with younger wines from the row above, ensuring consistency and complexity over time."
    },
    {
        "question": "What are the options for enjoying wines at Jessup Cellars?",
        "answer": "Jessup Cellars offers wines by the glass or bottle, and several tasting flight experiences, including the Light Flight and Jessup Classic Tasting."
    },
    {
        "question": "What does the Light Flight tasting experience at Jessup Cellars include?",
        "answer": "The Light Flight includes 3 wines, starting with the 2022 Chardonnay and two of the most requested red wines. It costs $30 per person, with the tasting fee waived for wine purchases over $50."
    },
    {
        "question": "What does the Jessup Classic Tasting experience include?",
        "answer": "The Jessup Classic Tasting includes a flight of 5 wines paired with cheeses, Marcona almonds, and a chocolate surprise. It costs $60 per person, waived with the purchase of two or more bottles of wine per person."
    },
    {
        "question": "What virtual tasting experiences does Jessup Cellars offer?",
        "answer": "Jessup Cellars offers a virtual tasting experience where a wine educator guides you through a tasting via Zoom. You can invite friends, family, and co-workers, and the virtual tasting fee is reimbursed with certain wine purchases."
    },
    {
        "question": "How can you enjoy a personalized tasting experience from Jessup Cellars at home?",
        "answer": "A Jessup Cellars Wine Educator can travel to your home or business to host a tasting for your friends and colleagues. This experience is complimentary once everyone purchases 3 to 4 bottles."
    },
    {
        "question": "What is the Petit Tasting experience from Jessup Cellars?",
        "answer": "The Petit Tasting is ideal for groups up to 12 guests and includes six wines from the Jessup Cellars portfolio. It requires a minimum purchase and a refundable $700 Booking fee for members, and a refundable $1600 Event fee for non-members."
    },
    {
        "question": "What does the Grand Tasting experience from Jessup Cellars include?",
        "answer": "The Grand Tasting includes 12 bottles of wine and can fit any setting. Members require a minimum purchase and a refundable $350 Booking fee, while non-members require a refundable $2200 Event fee."
    },
    {
        "question": "What is the Soirée Tasting experience from Jessup Cellars?",
        "answer": "The Soirée Tasting is ideal for large groups and includes 4 to 5 bottles each of four different wines. Members require a minimum purchase and a refundable $350 Booking fee, while non-members require a refundable $2800 Event fee."
    },
    {
        "question": "How can you schedule a private tasting experience with Jessup Cellars?",
        "answer": "You can schedule a private tasting experience with Jessup Cellars by visiting their website at https://jessupcellars.com/in-home-wine-tastings/."
    },
    {
        "question": "What benefits do Jessup Cellars wine club members receive?",
        "answer": "Jessup Cellars wine club members receive a 15% discount on all current release orders, invitations to 'Members Only' special events, and free tastings a couple of times per year with up to 4 guests in the Yountville Tasting Gallery."
    },
    {
        "question": "How many membership options does Jessup Cellars offer?",
        "answer": "Jessup Cellars offers three membership options: Tasting Club, My Jessup Cellar 6, and My Jessup Cellar 12."
    },
    {
        "question": "What does the Tasting Club membership include?",
        "answer": "The Tasting Club membership delivers 3 bottles of wine curated by the Jessup Cellars team four times per year. Members can choose to have their wines shipped to their home or business, or they can pick up their wines at the Yountville tasting room. The average cost of each shipment is approximately $200 plus shipping."
    },
    {
        "question": "How much does the Tasting Club membership cost?",
        "answer": "The average cost of each Tasting Club shipment is approximately $200 plus shipping, which varies by region and shipping method."
    },
    {
        "question": "What is included in the My Jessup Cellar 6 membership?",
        "answer": "The My Jessup Cellar 6 membership delivers 6 bottles of wine twice per year in April and September. Members can choose their wines in advance and define the cost based on their selections. The typical cost is about $400 twice per year plus shipping."
    },
    {
        "question": "How much does the My Jessup Cellar 6 membership cost?",
        "answer": "The typical cost for the My Jessup Cellar 6 membership is about $400 twice per year plus shipping, which varies by region and shipping method."
    },
    {
        "question": "What is included in the My Jessup Cellar 12 membership?",
        "answer": "The My Jessup Cellar 12 membership includes 12 bottles of wine twice per year in April and September. The average cost per shipment is $800. Members also receive $20 flat rate shipping anywhere in the lower 48 states."
    },
    {
        "question": "How much does the My Jessup Cellar 12 membership cost?",
        "answer": "The average cost for the My Jessup Cellar 12 membership is $800 per shipment."
    },
    {
        "question": "Do Jessup Cellars wine clubs have membership fees?",
        "answer": "No, Jessup Cellars wine clubs do not have membership fees."
    },
    {
        "question": "What discounts do Jessup Cellars wine club members receive on wine purchases?",
        "answer": "Jessup Cellars wine club members receive a 15% discount on all wine purchases and re-orders."
    },
    {
        "question": "What additional benefit do My Jessup Cellar 12 members receive?",
        "answer": "My Jessup Cellar 12 members receive $20 flat rate shipping anywhere in the lower 48 states."
    },
    {
        "question": "What free tasting benefits do wine club members receive?",
        "answer": "Wine club members receive free tastings a couple of times per year with up to 4 guests in the Yountville Tasting Gallery."
    },
    {
        "question": "What happens if a guest becomes a member during a tasting at Jessup Cellars?",
        "answer": "If a guest becomes a member during a tasting at Jessup Cellars, the current member receives a $25 gift card."
    },
    {
        "question": "What certification does Bardessono Hotel and Spa have?",
        "answer": "Bardessono Hotel and Spa is LEED Platinum-certified."
    },
    {
        "question": "What amenities does Bardessono Hotel and Spa offer?",
        "answer": "Bardessono Hotel and Spa offers luxurious suites with modern amenities, an on-site spa, and a farm-to-table restaurant."
    },
    {
        "question": "What features does Hotel Yountville have?",
        "answer": "Hotel Yountville features elegant rooms, lush gardens, a spa, and a renowned restaurant."
    },
    {
        "question": "Is Hotel Yountville within walking distance of downtown Yountville?",
        "answer": "Yes, Hotel Yountville is within walking distance of downtown Yountville."
    },
    {
        "question": "What accommodations does Vintage House provide?",
        "answer": "Vintage House provides spacious guest rooms, beautifully landscaped grounds, and a pool."
    },
    {
        "question": "What additional access does Vintage House offer?",
        "answer": "Vintage House offers access to the nearby Estate Yountville, which includes additional dining options and amenities."
    },
    {
        "question": "What is the style of North Block Hotel?",
        "answer": "North Block Hotel is Mediterranean-inspired."
    },
    {
        "question": "What amenities does North Block Hotel offer?",
        "answer": "North Block Hotel offers stylish accommodations, a tranquil courtyard, a pool, and a popular restaurant serving Italian cuisine."
    },
    {
        "question": "What special deal does North Block Hotel offer related to Jessup Cellars?",
        "answer": "North Block Hotel offers special deals on wine tasting at Jessup Cellars."
    },
    {
        "question": "What is included in The Estate Yountville?",
        "answer": "The Estate Yountville includes several luxury hotels such as Vintage House and Hotel Villagio, as well as upscale dining options, a spa, and event venues."
    },
    {
        "question": "What special offer does Napa Valley Lodge provide for Jessup Cellars?",
        "answer": "Napa Valley Lodge offers 2 for 1 tastings at Jessup Cellars."
    },
    {
        "question": "Where is Napa Valley Lodge located?",
        "answer": "Napa Valley Lodge is located on Highway 29, the main thoroughfare through Napa Valley."
    },
    {
        "question": "What type of views do many rooms at Napa Valley Lodge offer?",
        "answer": "Many rooms at Napa Valley Lodge offer views of the surrounding vineyards or the beautifully landscaped gardens."
    },
    {
        "question": "What amenities are available at Napa Valley Lodge?",
        "answer": "Napa Valley Lodge offers a heated outdoor pool and hot tub, a fitness center, and complimentary bicycle rentals."
    },
    {
        "question": "What is included in the daily breakfast at Napa Valley Lodge?",
        "answer": "The daily breakfast buffet at Napa Valley Lodge includes fresh pastries, fruit, yogurt, cereals, and hot items."
    },
    {
        "question": "Does Napa Valley Lodge offer concierge services?",
        "answer": "Yes, Napa Valley Lodge offers concierge services to help guests plan their stay, including arranging wine tastings, restaurant reservations, and transportation."
    },
    {
        "question": "Does Napa Valley Lodge have meeting and event space?",
        "answer": "Yes, Napa Valley Lodge offers meeting and event space for corporate gatherings, weddings, and other special occasions."
    },
    {
        "question": "What is the setting of Napa Valley Lodge?",
        "answer": "Napa Valley Lodge is set overlooking one of Grgich Hills vineyards."
    },
    {
        "question": "Which Thomas Keller restaurant in Yountville is known for its exquisite tasting menus?",
        "answer": "The French Laundry is known for its exquisite tasting menus, impeccable service, and award-winning wine list."
    },
    {
        "question": "Where is The French Laundry located?",
        "answer": "The French Laundry is housed in a historic stone building in Yountville."
    },
    {
        "question": "What type of cuisine does Bouchon Bistro serve?",
        "answer": "Bouchon Bistro serves classic French bistro fare."
    },
    {
        "question": "Where is Bouchon Bistro located in relation to The French Laundry?",
        "answer": "Bouchon Bistro is located across the street from The French Laundry."
    },
    {
        "question": "What does Bouchon Bakery offer?",
        "answer": "Bouchon Bakery offers artisanal breads, pastries, sandwiches, desserts, coffee, and espresso drinks."
    },
    {
        "question": "What is Bouchon Bakery popular for?",
        "answer": "Bouchon Bakery is popular for breakfast, lunch, and afternoon snacks."
    },
    {
        "question": "What type of dining experience does Ad Hoc offer?",
        "answer": "Ad Hoc offers a casual dining experience with a focus on family-style meals."
    },
    {
        "question": "What is Ad Hoc famous for on Monday evenings?",
        "answer": "Ad Hoc is famous for its fried chicken on Monday evenings."
    },
    {
        "question": "What is the focus of the menu at RO Restaurant and Lounge?",
        "answer": "The menu at RO Restaurant and Lounge focuses on Asian-inspired cuisine, wine, cocktails, and a large selection of Champagne and sparkling wines."
    },
    {
        "question": "What type of cuisine does La Calenda offer?",
        "answer": "La Calenda offers Mexican cuisine inspired by the rich culinary traditions of Oaxaca, Mexico."
    },
    {
        "question": "What dishes are recommended at La Calenda?",
        "answer": "It's recommended to try the Mole and margaritas at La Calenda."
    },
    {
        "question": "What type of cuisine does Bistro Jeanty serve?",
        "answer": "Bistro Jeanty serves authentic French cuisine."
    },
    {
        "question": "What dish is a must-try at Bistro Jeanty?",
        "answer": "The tomato bisque in puff pastry is a must-try at Bistro Jeanty."
    },
    {
        "question": "What type of cuisine does Lucy Restaurant & Bar offer?",
        "answer": "Lucy Restaurant & Bar offers farm-to-table California cuisine with a focus on fresh, locally sourced ingredients."
    },
    {
        "question": "When is it best to visit Lucy Restaurant & Bar for breakfast?",
        "answer": "It's best to visit Lucy Restaurant & Bar for brunch on weekends."
    },
    {
        "question": "What type of cuisine does Ciccio offer?",
        "answer": "Ciccio offers contemporary Italian cuisine with a focus on fresh, seasonal ingredients."
    },
    {
        "question": "What are some staples on the menu at Ciccio?",
        "answer": "Pasta, pizza, seafood, and meat dishes are staples on the menu at Ciccio."
    },
    {
        "question": "What kind of views can you enjoy at R&D Kitchen?",
        "answer": "You can enjoy stunning vineyard views from R&D Kitchen."
    },
    {
        "question": "What type of cuisine does R&D Kitchen offer?",
        "answer": "R&D Kitchen offers sophisticated and fresh cuisine inspired by California’s indoor/outdoor culture."
    },
    {
        "question": "What is a popular drink to have at R&D Kitchen?",
        "answer": "One of the best margaritas in town can be found at R&D Kitchen."
    },
    {
        "question": "What type of dining experience does Bottega offer?",
        "answer": "Bottega offers an unmistakably Italian dining experience with a stunning Napa Valley setting."
    },
    {
        "question": "What are some features of the indoor setting at Bottega?",
        "answer": "Inside Bottega, you’ll find Venetian plaster, Murano glass chandeliers, soft leather chairs, and ample tables."
    },
    {
        "question": "What does 'Ottimo' mean in Italian?",
        "answer": "'Ottimo' means optimal, first rate, or excellent in Italian."
    },
    {
        "question": "What does Michael Chiarello share at Ottimo?",
        "answer": "Michael Chiarello shares pizzas, fresh mozzarella, coffee, wine, beer, and handcrafted products at Ottimo."
    },
    {
        "question": "What cuisine does Coqueta Napa Valley explore and interpret?",
        "answer": "Coqueta Napa Valley explores and interprets Spanish cuisine."
    },
    {
        "question": "What does 'Coqueta' mean in Spanish?",
        "answer": "'Coqueta' means 'flirt' or 'infatuation' in Spanish."
    },
    {
        "question": "What is the RH Restaurant at RH Yountville part of?",
        "answer": "The RH Restaurant is part of the five-building RH Yountville compound."
    },
    {
        "question": "What does RH Restaurant at RH Yountville integrate?",
        "answer": "RH Restaurant integrates food, wine, art, and design."
    },
    {
        "question": "What type of cuisine does The Kitchen at Priest Ranch combine?",
        "answer": "The Kitchen at Priest Ranch combines the vibrant flavors of seasonal American cuisine with regional influences of the Midwest."
    },
    {
        "question": "What is the atmosphere like at The Kitchen at Priest Ranch?",
        "answer": "The Kitchen at Priest Ranch offers a warm and inviting atmosphere."
    },
    {
        "question": "What is Kollar Chocolates known for?",
        "answer": "Kollar Chocolates is known for its award-winning artisan chocolates."
    },
    {
        "question": "What accolades has Kollar Chocolates received?",
        "answer": "Kollar Chocolates was named one of the TOP 10 CHOCOLATIERS OF NORTH AMERICA by Dessert Professional Magazine and was featured in Oprah’s O Magazine."
    },
    {
        "question": "What does Madeleine's Macarons offer?",
        "answer": "Madeleine's Macarons offers handmade French macarons, breakfast and lunch crepes, coffee, and house-made ice cream with local fresh ingredients."
    },
    {
        "question": "What is The Model Bakery known for?",
        "answer": "The Model Bakery is known for its breads, pastries, and coffee."
    },
    {
        "question": "Where is The Model Bakery located in Yountville?",
        "answer": "The Model Bakery in Yountville is located in the Caboose at the Railroad Inn Yountville."
    },
    {
        "question": "What is the history of Ranch Market Too?",
        "answer": "Ranch Market Too was opened by the Housley family in July 1977 in Yountville."
    },
    {
        "question": "What deli business operates independently in the Yountville store?",
        "answer": "Velo Pizza and Deli operates independently in the Yountville store, offering pizza by the slice and great deli sandwiches."
    },
    {
        "question": "Are dogs allowed at Jessup Cellars?",
        "answer": "Jessup Cellars welcomes your well-behaved dogs inside or outside and we have gluten free dog treats available as well as water dishes."
    },
    {
        "question": "What makes Jessup Cellars wines special?",
        "answer": "Jessup Cellars wines are carefully crafted with the help of our renowned consulting winemaker Rob Lloyd who famously crafted Chardonnay for Rombauer, La Crema and Cakebread. Not only has Rob created one of the best Chardonnays in the Napa Valley with our 2022 vintage, but has also helped curate 'The Art of the Blend' with our stellar red wines."
    },
    {
        "question": "What white wines does Jessup Cellars offer?",
        "answer": "Our leading white wine is our Napa Valley Chardonnay from the Los Carneros region. The Truchard Vineyard is perfectly located in the hills above Highway 12 with the San Francisco Bay influences creating a cooler growing climate where the grapes ripen slowly and perfectly on the vine. The perfect weather combines with an ideal terroir to create the foundation for a well-balanced Chardonnay aged for 10 months in 40% new American Oak barrels. We also offer an annual harvest of Sauvignon Blanc which is sourced from North Coast vines outside of the Napa Valley. The tropical nature of our 2023 Sauvignon Blanc is decidedly different than the typical Sauvignon Blanc grown in the Valley and elsewhere in the World. Due to its limited supply this wine sells out quickly each year so be sure to give us a call before visiting our tasting room to check availability."
    },
    {
        "question": "Tell me about white wine?",
        "answer": "Our leading white wine is our Napa Valley Chardonnay from the Los Carneros region. The Truchard Vineyard is perfectly located in the hills above Highway 12 with the San Francisco Bay influences creating a cooler growing climate where the grapes ripen slowly and perfectly on the vine. The perfect weather combines with an ideal terroir to create the foundation for a well-balanced Chardonnay aged for 10 months in 40% new American Oak barrels."
    },
    {
        "question": "Can you tell me more about your 2022 Chardonnay?",
        "answer": "The Jessup Cellars 2022 Chardonnay is a white wine that comes across as very well balanced due to the aging being done in a combination of 40% new American and 60% neutral American Oak. This brings hints of oak to the wine while also offering a slightly creamy mouth feel without being a butter bomb. Our Napa Valley Chardonnay is a member favorite while the non-member price of $55 is appreciated by enthusiasts of this quality wine crafted by Rob Lloyd. The alcohol content is 14.8% while the PH is 3.4."
    },
    {
        "question": "Tell me about your 2023 Sauvignon Blanc?",
        "answer": "Our 2023 vintage is 100% Sauvignon Blanc sourced from North Coast vineyards aged in 100% stainless steel barrels which is typical for this varietal. The stainless steel seals out the oxygen and seals in the flavors of the fruit and is a hearty 15.1% alcohol content with a PH of 3.3. While it's nose and flavors hint at tropical delights, we would not consider this wine to be too fruit forward, but rather fruit balanced with hints of pineapple and mango. Our Sauvignon Blanc is the perfect hot tub wine or for those warm summer evenings after a long day in the hot summer Sun. You will feel refreshed after enoying a glass or two of our Sauvignon Blanc, non-member price of $45!\n\nThe 2023 Sauvignon Blanc pairs wonderfully with a variety of dishes, enhancing the dining experience. For starters, it complements the flavors of Grilled Prawn Cocktail and Ceviche, accentuating the seafood's delicate taste and brightening the citrus elements in the dishes. The wine's fruity and floral notes beautifully complement the freshness of Tacos, making it an ideal match for this flavorful and versatile Mexican dish. Lastly, the wine's high acidity and fruit-forward character provide a delightful contrast to the creamy sweetness of a Peach & Burrata salad, creating a harmonious and memorable pairing."
    },
    {
        "question": "What does your white wine pair well with?",
        "answer": "Our white wine pairs well with a variety of dishes, enhancing the dining experience. For starters, it complements the flavors of Grilled Prawn Cocktail and Ceviche, accentuating the seafood's delicate taste and brightening the citrus elements in the dishes."
    },
    {
        "question": "What white wines do you have?",
        "answer": "We offer the following wines: The Jessup Cellars 2022 Chardonnay and the 2023  Sauvignon Blanc"
    },
    {
        "question": "What red wines is Jessup Cellars offering in 2024?",
        "answer": "Jessup Cellars offers a number of red wines across a range of varietals, from Pinot Noir and Merlot blends from the Truchard Vineyard, to blended Cabernet Sauvignon from both the Napa and Alexander Valleys, our Mendocino Rougette combining Grenache and Carignane varietals which we refer to as our 'Summer Red', to the ultimate expression of the 'Art of the Blend\" with our Juel and Table for Four Red Wines. We also offer 100% Zinfandel from 134 year old vines in the Mendocino region and our own 100% Petite Sirah grown in the Wooden Valley in Southeastern Napa County. We also offer some seasonal favorites, led by the popular whimsical Manny's Blend which should be released later in 2024 with a very special label."
    },
    {
        "question": "Please tell me more about your consulting winemaker Rob Lloyd?",
        "answer": "Rob Lloyd \nConsulting Winemaker\n\nBIOGRAPHY\nHometown: All of California\n\nFavorite Jessup Wine Pairing: Carneros Chardonnay with freshly caught Mahi-Mahi\n\nAbout: Rob\u2019s foray into wine started directly after graduating college when he came to Napa to work in a tasting room for the summer \u2013 before getting a \u2018real job\u2019. He became fascinated with wine and the science of winemaking and began to learn everything he could about the process.\n\nWhile interviewing for that \u201creal job\u201d, the interviewer asked him what he had been doing with his time since graduation. After speaking passionately and at length about wine, the interviewer said, \u201cYou seem to love that so much. Why do you want this job?\u201d Rob realized he didn't want it, actually. He thanked the man, and thus began a career in the wine industry.\n\nRob has since earned his MS in Viticulture & Enology from the University of California Davis and worked for many prestigious wineries including Cakebread, Stag\u2019s Leap Wine Cellars, and La Crema. Rob began crafting Jessup Cellars in the 2009 season and took the position of Director of Winemaking at Jessup Cellars in 2010. He now heads up our winemaking for the Good Life Wine Collective, which also includes Handwritten Wines."
    },
    {
        "question": "Tell me an interesting fact about Rob Llyod",
        "answer": "While interviewing for that \u201creal job\u201d, the interviewer asked him what he had been doing with his time since graduation. After speaking passionately and at length about wine, the interviewer said, \u201cYou seem to love that so much. Why do you want this job?\u201d Rob realized he didn't want it, actually. He thanked the man, and thus began a career in the wine industry."
    },
    {
        "question": "Who is your winemaker at the winery in Napa?",
        "answer": "Bernardo Munoz\nWinemaker\n\nBIOGRAPHY\nHometown: Campeche, Mex\n\nFavorite Jessup Wine Pairing: 2010 Manny\u2019s Blend with Mongolian Pork Chops from Mustards Grill \u2013 richness paired with richness\n\nAbout: Bernardo began his career in the vineyards, learning the intricacies of grape growing and how to adjust to the whims of Mother Nature. He then moved into the cellars at Jessup Cellars, bringing us his complete grape to bottle knowledge to the team. He has a keen understanding of what it takes to make a great bottle."
    },
    {
        "question": "What can you tell me about your Pinot Noir?",
        "answer": "What makes our Pinot Noir unique from typical Pinot is the added element of the Jessup 'Art of the Blend'. While it is 96.7% Pinot Noir with fruit sourced from our favorite Los Carneros Truchard Vineyard, our master winemakers blend in a little (3.3%) of our own Petite Sirah from our estate vineyard in the Wooden Valley area of Southeastern Napa County and age it in 50% new French oak for 10 months The alcohol content of this vintage is 14.8% with a PH of 3.45.This gives our 2021  Pinot Noir a much bolder color, very different from your typical light and bright Pinot you may be accustomed to. This also adds body to the wine which has become a member favorite at Jessup Cellars, priced at $70 for non-members. "
    },
    {
        "question": "Tell me more information about your 2019 Merlot?",
        "answer": "Our 2019 Jessup Cellars Merlot is from the Truchard Vineyard in the Los Carneros region of the Napa Valley which enjoys the San Francisco Bay influences that also envelope our Chardonnay and Pinot Noir. The terroir is ideally suited for a full bodied Merlot and like many of our wines, our Merlot is reflective of the 'Art of the Blend' by our winemakers. The 2019 Merlot is 80% Merlot, 16.5% Cabernet Sauvignon from the Chiles Valley AVA in Northeastern Napa County and a splash of our Petite Sirah (3.5%) from the same location finishes the wine perfectly. Our merlot is aged for 22 months in 40% new American/French oak with an alcohol content of 15.1% with a PH level of 3.55. This wine drinks well now, however, will continue to age gracefully for another 5-8 years.  We recommend trying this delicious Merlot with roasted chicken and vegetables or beef bourguignon. Non-members can pick up our 2019 Napa Valley Merlot for $70."
    },
    {
        "question": "What makes your 2020 Pacini Vineyards Zinfandel special?",
        "answer": "Jessup Cellars has a history of making fine big Zinfandels, but the 2020 Pacini Vineyards 100% Zinfandel from the Talmage Bench in Mendocino County is decidedly different than your typical Zin, with the grapes for this wine coming from 134 year old \"ancient vines\". Brimming with nuances of ripe cranberry, pomegranate, cherry cola, white pepper, and vanilla, this wine offers soft tannins with a nice, long finish. This wine is aged in used (neutral) Chardonnay barrels with an alcohol content of 14.9%. The price is $60 for non-members.\n\nPair with pastas, barbequed meats or just pour yourself a glass and enjoy on its own. \n\nDrink now after decanting or age for up to 9 years. "
    },
    {
        "question": "Does Jessup Cellars offer Napa Valley Cabernet Sauvignon?",
        "answer": "Napa Valley Cabernet Sauvignon is a staple of most Napa Valley winemakers with Jessup offering our 2019 Cabernet Sauvignon for 2024. As with most of our red wines, our winemakers exercise 'The Art of the Blend' by starting with 90% Napa Valley fruit from the Chiles Valley AVA in Northeastern Napa County, then blend in 5% Petite Sirah from the same AVA, 3% Merlot from our Truchard Vineyard in the Los Carneros region, then finish it with 2.1% Cabernet Franc, which is the parent grape of both Cabernet Sauvignon and Merlot, often used in blended wines. Cabernet Franc originated in the Bordeaux region of France and to honor that provenance, we age our 2019 Jessup Cellars Cabernet Sauvignon in 80% new French oak for 22 months. Alcohol content in this varietal is14.9% with a PH of 3.65. You can purchase our 2019 Cab for $90.\n\nThe palate of the wine matches the aromatics providing juicy fruit flavors, rich tannins and a long finish.  This wine drinks well now however will age gracefully for the next 5-8 years.  \n\nEnjoy this Cabernet Sauvignon with a quality cut of beef or any dish that has a nice smoky/fatty/or charred quality. "
    },
    {
        "question": "Besides Napa Valley Cabernet Sauvignon, does Jessup Cellars offer other Cabernets?",
        "answer": "Jessup Cellars has created a 2018 Alexander Valley Cabernet Sauvignon with 96.5% Cabernet grapes, finished with 3.5% Napa Valley Petite Sirah fruit. This wine has a very different nose and mouth feel than our 2019 Cabernet, presenting a dry, more tannic finish which still feels young but full bodied as it crosses your palate. You could lay this bottle down for another 5-8 years as you wait for it to soften, but if you want to drink it now, we encourage you to pair this wine with a nice Filet Mignon or other red meat. Our Alexander Valley Cabernet is aged in 80% new French oak with an alcohol content of 14.9% and may be purchased for $90 for non-members."
    },
    {
        "question": "What varietal grapes are in your Rougette wine?",
        "answer": "Jessup Cellars 2019 Rougette is the perfect blend of Spanish varietals including 87% Grenache and 13% Carignane, both coming from our Mendocino growing region which is particularly suited for what we refer to as our 'Summer Red'. This beautiful wine of co-fermented Grenache and Carignane varieties greets you with opulent aromas of sweet strawberry, ripe cranberry jam, red plum, cassis, and nutmeg. We aghe this wine by co-fermenting the varietals for 15 months in used (neutral) Chardonnay barrels and delivers a 14.9% alcohol content with a PH of 3.35. The non-member price is $60.\n\nThe palate is wonderfully dry and lifted with fresh acidity and silky, rich tannins. Flavors of brambly, ripe fruit make this wine exceptionally palatable and food-friendly. \n\nEnjoy it with duck confit, mushroom risotto or an assortment of softer cheeses. Drink now or cellar 2-3 years."
    },
    {
        "question": "What is different about your 2018 Rougette versus the 2019?",
        "answer": "This beautiful Jessup Cellars 2018 Rougette, comprised of our Mendocino Grenache and a touch of Carignane from the Dry Creek AVA in Sonoma County, showcases ripe red cherries, plums, cranberries, fig jam, and a hint of holiday baking spices. The palate is wonderfully dry with fresh acidity and balanced with fine-grained tannins that blend perfectly with the brambly fruit characteristics. This wine will age nicely for 5-7 years and will pair nicely with an array of dishes, especially those that grace our tables during the joyous holiday season including turkey, ham and all the fixings. Like our 2019 Rougette, this vintage is aged in used Chardonnay barrels and shares the same 14.9% alcohol content. It is priced at $70 for non-members."
    },
    {
        "question": "What is the varietal mix for your Juel Red blend?",
        "answer": "Jessup Cellars 2019 Juel Red Wine is one exploration of the ultimate 'Art of the Blend' expression. Juel is named in homage to the Father of one of our owner families which is of Swiss origin. Our winemakers have built a Jessup favorite with this wine comprised of 56% Napa Valley Cabernet Sauvignon and 14% Cabernet Franc, with Merlot figuring heravily into the blend at 24% from our Truchard Vineyard fruit. The wine is finished with 2% each of Petite Sirah, Petite Verdot and Malbec, all from the Napa Valley. Jessup Cellars' 2019 \"Juel\" Blend is a harmonious composition of varietals, a testament to the artistry of winemaking. This wine is a celebration of balance, with its blend of dark fruit, baking spices, and earthy elements coming together in perfect unison. Approachable yet age-worthy, \"Juel\" is a sensory journey that invites you to savor the intricacies of each sip. Pour a glass, and let the symphony unfold. The non-member price for Juel is $115.\n\nJuel is aged in 70% new French oak for 22 months with 14.9% alcohol by volume. The PH is 3.65."
    },
    {
        "question": "Composition of Juel Red blend",
        "answer": "56% Napa Valley Cabernet Sauvignon and 14% Cabernet Franc, with Merlot figuring heravily into the blend at 24% from our Truchard Vineyard fruit. The wine is finished with 2% each of Petite Sirah, Petite Verdot and Malbec, all from the Napa Valley. Jessup Cellars' 2019 \"Juel\" Blend is a harmonious composition of varietals, a testament to the artistry of winemaking. Juel is aged in 70% new French oak for 22 months with 14.9% alcohol by volume. The PH is 3.65."
    },
    {
        "question": "What is the difference between Jessup Table for Four Red Wine and Juel?",
        "answer": "Table for Four is our celebrated and signature Cabernet Sauvignon-based blend and is anxiously anticipated by both guests and staff alike each year upon its release. Our 2019 vintage carries on the tradition of comprising a wine of distinction and depth, with layers of complexity to titillate any wine enthusiast.\n\nWith notes of ripe black cherry and blackberry on the nose, the luscious fruit is accompanied by warm and inviting aromas of baking spice and dark cacao. An intriguing layer of subtle floral and herbal undertones enhances the complexity, with violet, anise, and a hint of spearmint adding nuance to this incredible profile.\n\nThe palate sings with harmony as the fruit and spice components interplay, and fine, compact tannins give this wine the structural integrity to age for many years to come. With a lovely lingering finish, enjoy this wine now for a vibrant experience on the palate, or cellar it to increase its nuance in years to come.\n\nWhile Jessup Cellars Table for Four is comprised of the same 6 varietals as our Juel, the blend is very different being more Cab forward with 61.8% Cabernet, Sauvignon and 26.5% Cabernet Franc, expertly finished with 4.2% Petite Verdot, 3.5% Petite Sirah, 2.7% Malbec and and a hint of Merlot at 1.1%.Like pur Juel the Table for Four is aged in 70% new French oak and matches the alcohol content at 14.9% as well as the PH at 3.65. The rice for non-members is $115."
    },
    {
        "question": "Does Jessup Cellars offer a 100% Petite Sirah?",
        "answer": "Jessup Cellars has introduced our first estate grown 100% Petite Sirah beginning with the 2021 vintage as a standalone wine, while also using it extensively in our 'Art of the Blend' winemaking process going forward.  \n\nOur 2021 Petite Sirah offers a captivating sensory journey with a complex blend of flavors and aromas. The wine opens with luscious notes of blueberry and tart cherry, creating a vibrant and fruity introduction. Pomegranate adds a touch of brightness, complemented by the subtle sweetness of brown sugar and the deep richness of cassis.\n\nThe influence of bourbon and sour mash emerges, contributing a layer of complexity with hints of oak and a delightful cake batter essence. Notes of plum jam adds a comforting touch of sweetness, while cracked pepper brings a subtle spice that enhances the overall profile.\n\nThe wine showcases robust yet approachable tannins, providing a structured backbone that promises aging potential. Bright acidity adds a refreshing quality, balancing the richness of the fruit and contributing to the wine's overall harmony. The finish is long and satisfying, leaving lingering impressions of cedar, licorice, and the delicate essence of raspberry. To say the least, there is a lot going on with this sublime wine. This wine is aged for 22 months in a mix of used (neutral) French and American barrels and is our \"hottest\" wine with an alcohol content of 15.6% with a PH of 3.65.\n\nOur estate vineyard in the Wooden Valley of Southeastern Napa County will be the foundation for our continued growth in the Napa Valley."
    },
    {
        "question": "Does Jessup Cellars have fortified and Port style wines?",
        "answer": "Jessup Cellars makes a few fortified vintages of their Zinfandel  Port and offers a 100% Cabernet Sauvignon dessert wine."
    },
    {
        "question": "What is the current Zinfandel Port release?",
        "answer": "Jessup Cellars is currently offering our 2013 100% Zinfandel Port fortified with Brandy.   Some of the most unique and long-lived wines in the World are Port wines. Paying homage to tradition, Jessup Cellars has always been known for making quality small batches of Port style wines from Zinfandel and Cabernet Sauvignon grapes. The 2013 Zinfandel Port is just another phenomenal addition to that family. Boasting bold aromatics of ripe rasberry, leather, and spice on the nose, followed by vanilla and red plum that dances on the palate. The finish is strong yet balanced making this a perfect match for blue cheese, dark chocolate or a Maduro cigar. Drink now or cellar for 7-10 years. This delicious wine has an alcohol content of 19.5%, so a litttle goes a long way. Pricing is $65 dollars for non-members."
    },
    {
        "question": "What is unique about the 13th Reflection Tawny dessert wine?",
        "answer": "Crafted in the traditional Solera method, this rich and lush dessert wine offers pronounced aromas of stewed cherry, dried fig, chocolate, and baking spice with a kiss of sandalwood and cedar.\n\nA decadent and juicy palate of mixed berry preserves will make a perfect digestif after a rich meal. Deliciously sweet yet fresh,this wine will pair with desserts like chocolate lava cake or a cheese course of ripe, aged, salty cheeses. Enjoy it now or cellar for 10-15 years. \n\nThe Infinite Reflection 13th Recursion is 100% Napa Valley Cabernet Sauvignon aged for 12 years in French oak with an alcohol content of 19.5%. Non-members may purchase this wine for $85."
    },
    {
        "question": "What is the Solera method of dessert wine creation?",
        "answer": "The Solera method is a traditional aging and blending process commonly used in the production of fortified wines, including dessert wines like Sherry and Madeira. Here's how it works:\nTiered Stacking: The process begins with a series of barrels or casks arranged in a tiered system called a \"solera stack.\" The bottom row contains the oldest wine, while subsequent rows contain progressively younger wines.\nFractional Blending: Each year, a portion of wine is drawn from the bottom row of barrels for bottling. This creates space in those barrels, which are then topped up with wine from the row above. The process continues up the stack, with each barrel being partially emptied and then replenished with younger wine.\nAging and Maturity: Because the barrels are only partially emptied each year, a portion of the older wine always remains in the barrels, contributing to the complexity and depth of flavor. Over time, the younger wines gradually blend with and inherit characteristics from the older wines.\nConsistency: The Solera method ensures consistency in the final product, as the blend of wines remains relatively constant over time. Even though some wine is removed for bottling each year, the overall character of the solera remains consistent due to the blending of older and younger wines.\nPerpetual Process: The Solera system is designed to be perpetual, with new wine continuously added at the top and matured wine drawn from the bottom for bottling. This allows producers to maintain a consistent product while also ensuring that some of the original wine remains in the solera stack, sometimes for many years or even decades.\nOverall, the Solera method is a meticulous and time-honored process that results in complex, well-balanced dessert wines with layers of flavor and aroma."
    },
    {
        "question": "What tasting experiences are available at Jessup Cellars?",
        "answer": "Jessup Cellars offers many experiences for enjoying our wines. You may enjoy wine by the glass or by the bottle, but most popular are our tasting flights. Our Light Flight includes 3 wines, starting with either our 2022 Chardonnay or our 2021 Pinot Noir. The cost per person is $30, and each tasting fee will be waived for each purchase of wine over $50. Walk-ins are welcome anytime for our Light Flight experience. Our most popular tastinig experience is the jessup Classic Tasting, which includes a flight of 5 wines perfectly paired with cheeses, accompanied by palate cleansing Marcona almonds and a chocolate surprise. The Classic Tasting is $60 perperson, but is waived with a purchase of two or more bottles of wine per person."
    },
    {
        "question": "what is the most popular tasting experience?",
        "answer": "Our most popular tastinig experience is the jessup Classic Tasting, which includes a flight of 5 wines perfectly paired with cheeses, accompanied by palate cleansing Marcona almonds and a chocolate surprise. The Classic Tasting is $60 perperson, but is waived with a purchase of two or more bottles of wine per person."
    },
    {
        "question": "Are walk ins allowed?",
        "answer": " Walk-ins are welcome anytime for our Light Flight experience. Our most popular tastinig experience is the jessup Classic Tasting, which includes a flight of 5 wines perfectly paired with cheeses, accompanied by palate cleansing Marcona almonds and a chocolate surprise. The Classic Tasting is $60 perperson, but is waived with a purchase of two or more bottles of wine per person."
    },
    {
        "question": "Are there in-home tasting experiences available from Jessup Cellars?",
        "answer": "Jessup Cellars offers \"Wine on Location\" tasting experiences nearly anywhere in the lower 48 states in the U.S. \nWine Tasting In Your Dining Room! A Jessup Cellars Wine Educator will travel to your home and host a tasting for your friends & colleagues! And\u2026 it\u2019s complimentary once everyone purchases 3 to 4 bottles. Navigate to https://jessupcellars.com/in-home-wine-tastings/ to learn more and schedule your private tasting experience with your friends, family or colleagues. Throughout the year our passionate educator, Adrienne, travels nationwide crafting exceptional Jessup Cellars Experiences. Forget about coordinating a whole trip to Napa Valley \u2013 our tasting room is now in your dining room."
    },
    {
        "question": "Do you offer memberships?",
        "answer": "Jessup Cellars offers 3 different membership options, providing flexible quantities and choices of wines with no member fees:\nThe Tasting Club delivers 3 bottles of wine curated by our team four times per year which may be shipped to your home or business, or you always have the option to come pick up your wines at our Yountville tasting room. The average cost of each shipment is approximately $200 plus shipping which varies by region and shipping method.\nMy Jessup Cellar 6 membership offers 6 bottles twice per year in April and September and adds the benefit of choice to the program. You may choose your wines in advance and define the cost based on your selections. The typical Jessup Cellars 6 cost is about $400 twice per year plus shipping which varies by region and shipping method.\nFinally, My Jessup Cellar 12 includes 12 bottles of wine twice per year, also in April and September with an average cost per shipment of $800,and of course you always have the option to pick up your wines if you are in the area. The My Jessup 12 members also receive $20 flat rate shipping anywhere in the lower 48 states."
    },
    {
        "question": "Does Jessup Cellars offer wine club memberships?",
        "answer": "Jessup Cellars offers 3 different membership options, providing flexible quantities and choices of wines with no member fees:\nMy Jessup 3 delivers 3 bottles of wine curated by our team four times per year which may be shipped to your home or business, or you always have the option to come pick up your wines at our Yountville tasting room. The average cost of each shipment is approximately $200 plus shipping which varies by region and shipping method.\nMy Jessup Cellar 6 membership offers 6 bottles twice per year in April and September and adds the benefit of choice to the program. You may choose your wines in advance and define the cost based on your selections. The typical Jessup Cellars 6 cost is about $400 twice per year plus shipping which varies by region and shipping method.\nFinally, My Jessup Cellar 12 includes 12 bottles of wine twice per year, also in April and September with an average cost per shipment of $800,and of course you always have the option to pick up your wines if you are in the area. The My Jessup 12 members also receive $20 flat rate shipping anywhere in the lower 48 states.\nAll of our wine clubs offer the benefits of not only receiving a 15% discount on ALL wine purchases and re-orders, but also free tastings a couple of times per year with up to 4 guests in our Yountville Tasting Gallery. We also offer a $25 gift card if your guests become members while enjoying a tasting at our Jessup Cellars Tasting Room & Gallery."
    },
    {
        "question": "What hotels are located near Jessup Cellars?",
        "answer": "There are a number of beautiful hotels in Yountville, the home of Jessup Cellars tasting room, the oldest in Yountville. Yountville, California, located in Napa Valley, is known for its charming atmosphere, world-class dining, and luxury accommodations. Here are some notable hotels in Yountville:\n\nBardessono Hotel and Spa: This LEED Platinum-certified hotel offers luxurious suites with modern amenities, an on-site spa, and a farm-to-table restaurant.\nHotel Yountville: A boutique hotel featuring elegant rooms, lush gardens, a spa, and a renowned restaurant, all within walking distance of downtown Yountville.\nVintage House: A luxury hotel with spacious guest rooms, beautifully landscaped grounds, a pool, and access to the nearby Estate Yountville, which includes additional dining options and amenities.\nNorth Block Hotel: This Mediterranean-inspired hotel offers stylish accommodations, a tranquil courtyard, a pool, and a popular restaurant serving Italian cuisine and is directly across the street from Jessup Cellars and offers special deals on wine tasting at Jessup.\nThe Estate Yountville: A sprawling resort that includes several luxury hotels such as Vintage House and Hotel Villagio, as well as upscale dining options, a spa, and event venues.\nNapa Valley Lodge: The Napa Valley Lodge is a charming boutique hotel located in Yountville, California, at the heart of Napa Valley wine country and offers 2 for 1 tastings at Jessup Cellars.\n\nLocation: Situated on Highway 29, the main thoroughfare through Napa Valley, the Napa Valley Lodge offers convenient access to numerous wineries, restaurants, and attractions in Yountville and beyond.\nAccommodations: The lodge features spacious and well-appointed guest rooms and suites, each designed with comfort and relaxation in mind. Many rooms offer views of the surrounding vineyards or the beautifully landscaped gardens.\n"
    },
    {
        "question": "What amneties are available at Napa Valley Lodge?",
        "answer": "Amenities: Guests at the Napa Valley Lodge can enjoy a range of amenities, including a heated outdoor pool and hot tub, a fitness center, and complimentary bicycle rentals for exploring the local area.\nBreakfast: A complimentary breakfast buffet is served daily, featuring a selection of fresh pastries, fruit, yogurt, cereals, and hot items.\nConcierge Services: The lodge offers concierge services to help guests plan their stay, including arranging wine tastings, restaurant reservations, and transportation.\nMeeting and Event Space: The Napa Valley Lodge also offers meeting and event space for corporate gatherings, weddings, and other special occasions, with indoor and outdoor venues available.\nOverall, the Napa Valley Lodge provides a comfortable and welcoming retreat for visitors to Napa Valley, with its picturesque setting overlooking one of Grgich Hills vineyards.\n\nThese are just a few of the notable hotels in Yountville, each offering its own unique blend of luxury, comfort, and hospitality amidst the stunning backdrop of Napa Valley wine country."
    },
    {
        "question": "What Thomas Keller restaurants are located in Yountville?",
        "answer": "Thomas Keller, one of the most celebrated chefs in the world, has several restaurants in Yountville, California. Here are the Thomas Keller restaurants in Yountville:\n\nThe French Laundry: Arguably Keller's most famous restaurant, The French Laundry is a culinary icon known for its exquisite tasting menus, impeccable service, and award-winning wine list. The restaurant is housed in a historic stone building and offers a refined dining experience.\nBouchon Bistro: Located across the street from The French Laundry, Bouchon Bistro is a casual French brasserie serving classic bistro fare. The menu features dishes like steak frites, roast chicken, and seafood, as well as a selection of house-made pastries and desserts.\nBouchon Bakery: Adjacent to Bouchon Bistro, Bouchon Bakery offers a tempting array of artisanal breads, pastries, sandwiches, and desserts, as well as coffee and espresso drinks. The bakery is a popular spot for breakfast, lunch, and afternoon snacks.\nAdHoc: Ad Hoc is another renowned restaurant in Yountville, California, founded by Thomas Keller. Unlike The French Laundry or Bouchon, Ad Hoc offers a more casual dining experience with a focus on family-style meals and is famous for its fried chicken on Monday evenings which is served as part of the fixed-price, family-style dinner menu. However, it's always a good idea to check Ad Hoc's website or call ahead to confirm the schedule, as restaurant operations and special events may vary.\nRO Restaurant and Lounge: Formerly the Regiis Ova Caviar & Champagne Lounge has reopened as a whole new dinig spot in Yountville Alongside chef de cuisine Jeffery Hayashi, keller has created a fresh menu with a focus on Asian-inspired cuisine, as well as wine, cocktails and-yes-a large selection of Champagne and sparking.\nLa Calenda: Also located in Yountville, California, and it's indeed a remarkable addition to the culinary scene in Napa Valley. Another Thomas Keller creation, La Calenda is a Mexican restaurant inspired by the rich culinary traditions of Oaxaca, Mexico. It offers a modern take on classic Mexican dishes while honoring authentic flavors and techniques. Whatever you do, try the Mole and the margaritas!"
    },
    {
        "question": "What other restaurants of note are in Yountville?",
        "answer": "Bistro Jeanty: A beloved French bistro located in Yountville, California, known for its authentic French cuisine and charming ambiance. Bistro Jeanty offers a menu inspired by traditional French cooking, featuring dishes like coq au vin, cassoulet, escargot, steak frites, and more. The cuisine is hearty, comforting, and prepared with meticulous attention to detail. Don't miss the tomato bisque in puff pastry!\nLucy Restaurant & Bar: Lucy offers farm-to-table California cuisine with a focus on fresh, locally sourced ingredients. The menu features a variety of dishes inspired by the seasons, including salads, seafood, meats, and vegetarian options. You must try their brunch menu on weekends as it is the best breakfast in Yountville.\nCiccio: Ciccio offers contemporary Italian cuisine with a focus on fresh, seasonal ingredients. The menu features a variety of classic Italian dishes, as well as innovative interpretations of Italian favorites. Pasta, pizza, seafood, and meat dishes are all staples of the menu.\nR&D Kitchen:  Experience stunning vineyard views from this airy modern building. Featuring outdoor seating with relaxing adirondack chairs clustered around fire pits. R+D Kitchen brings sophisticated and fresh cuisine to a smart and convivial crowd. With a strong local following in each neighborhood, R+D is inspired by California\u2019s indoor/outdoor culture with spaces that are light filled and intimate in feel. Sit at the outdoor bar and enjoy the perfect Napa Valley weather while sipping on a glass of sauvignon blanc and sharing a dip duo with friends. If you are looking for a simple place to have one of the best margaritas in town look no further. R+D Kitchen\u2019s menu features fresh season ingredients and a little something for everyone from sushi to steak and sandwiches to salads. They also have amazing takout pizza at their To-Go location next door.\nBottega: Bottega offers an unmistakably Italian sense of style in a stunning Napa Valley setting. Dine outside on our expansive patio, complete with two stone fireplaces to warm you on the coolest Napa nights. Inside, you\u2019ll find a warm, rustic setting adorned with Venetian plaster, Murano glass chandeliers, soft leather chairs, and ample tables \u2014 the perfect atmosphere for a meal and an experience to remember.\nOttimo: In Italian, Ottimo means optimal, first rate, excellent. Michael Chiarello shares a lifetime of learning in the kitchen, with pizzas, fresh mozzarella, coffee, wine, beer, and handcrafted products.\nCoqueta Napa Valley: Coqueta means \u201cflirt\u201d or \u201cinfatuation\u201d in Spanish, and represents Michael Chiarello and his team\u2019s exploration and interpretation of Spanish Cuisine, wine and inspired cocktails, while highlighting the bounty of Northern California.\nRH Restaurant at RH Yountville :The RH Restaurant is part of the five-building RH Yountville compound located in the heart of Napa Valley. An integration of food, wine, art and design, the restaurant features timeless classics for brunch and dinner, as well as a selection of wines from esteemed vintners in the United States and Europe. RH Yountville also features a wine vault.\nThe Kitchen at Priest Ranch: Eat, Drink, Gather - The Kitchen at Priest Ranch combines the vibrant flavors of seasonal American cuisine with the regional influences of the Midwest. At The Kitchen, we source only the freshest locally grown ingredients to create high-quality, approachable dishes that showcase Napa Valley\u2019s bountiful produce in each bite. We believe that great food should be accessible to everyone, so we offer a warm and inviting atmosphere, making The Kitchen the perfect spot for a casual yet elevated experience."
    },
    {
        "question": "Are there any pastry or chocolate shops in Yountville?",
        "answer": "Fortunately there are a couple of great choices to satisfy your sweet tooth in Yountville.\nKollar Chocolates: Kollar Chocolates is an award-winning artisan chocolate shop in the heart of Yountville in the Napa Valley. Kollar Chocolates\u2019 mission is to elevate chocolate into a sensory experience driven by new world flavors, modern artistry, ethically sourced ingredients, and innovation. \nAccolades include... TOP 10 CHOCOLATIERS OF NORTH AMERICA by Dessert Professional Magazine\nFOOD NETWORK\u2019S CHOPPED WINNER 2020 - Episode 1, Season 42, \u201cSweet and Salty Success\u201d\nFEATURED IN OPRAH\u2019S O MAGAZINE - Easter Favorite Things, 2018\nMadeleine's Macarons: \"Handmade French Macarons from the heart of Napa Valley, breakfast and lunch crepes, the best coffee in town, and house made ice cream with local fresh ingredients!\"\nTHE MODEL BAKERY STORY: For close to 90 years, The Model Bakery has been part of the Napa Valley culinary scene, providing discerning and hungry residents and valley visitors the best breads, pastries and coffee house at the original location on Main Street in St. Helena. Karen Mitchell, once a successful caterer in the Napa Valley, has been the proprietor of The Model Bakery for nearly 30 years and the Model balery in Yountville is in the Caboose at the Railroad Inn Yountville.."
    },
    {
        "question": "Is there a market in Yountville?",
        "answer": "Ranch Market Too: In July 1977 the Housley's opened Ranch Market Too in Yountville, and in April 1996, their son, Arik Housley graduated from Pepperdine University and returned to the valley to take over the family businesses. In 2008, the deli business in the Yountville store was sold to become an independent deli which has since become Velo Pizza and Deli with pizza by the slice and great deli sandwiches."
    },
    {
        "question": "Where is Yountville?",
        "answer": "Yountville, California is located 9 miles north of Napa and 9 miles south of St. Helena in the center of the Napa Valley. You can reach Yountville by car from anywhere in the Northern California Bay Area in about an hour, while travelers from the Sacramento region will take about 1.5 hours. The are is served by multiple airports including SFO, Oakland, Sacramento and Santa Rosa."
    },
    {
        "question": "Where is Jessup Cellars?",
        "answer": "Jessup cellars and Tasting Gallery is located at 6740 Washinton St. at the North end of Yountville across from RH Yountville and North Block Restaurant. We are open from 10AM to 6PM 7 days a week and can be reached at 707.944.5620 for reservations and information."
    },
    {
        "question": "How do I find jessup Cellars online?",
        "answer": "Jessup Cellars can be found at https://jessupcellars.com/ where you may find directions, purchase wine or make reservations for tastings at our Yountville tasting room."
    }
]

# Load a pre-trained model for sentence embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load SpaCy's pre-trained model
nlp = spacy.load('en_core_web_sm')

# Extract question and answers from your QA pairs
corpus_questions = [qa['question'] for qa in qa_pairs]
corpus_answers = [qa['answer'] for qa in qa_pairs]

# Compute embeddings for each question
corpus_embeddings = model.encode(corpus_questions, convert_to_tensor=True)

# Threshold for determining if the question is out of corpus
similarity_threshold = 0.6

# Maintain conversation history with a limit
max_history_length = 20
conversation_history = []
entity_history = defaultdict(list)
last_entity = None

# Define follow-up triggers
follow_up_triggers = [
    "tell me more about it", "say more", "what do they have", "how much is it", "can you elaborate",
    "more information on", "details about", "info on", "tell me more", "can you tell me more"
]

def is_follow_up_query(query):
    return any(trigger in query.lower() for trigger in follow_up_triggers)

def update_conversation_history(user_input, bot_response):
    if len(conversation_history) >= max_history_length:
        conversation_history.pop(0)
    conversation_history.append({"message": user_input, "sender": "user"})
    conversation_history.append({"message": bot_response, "sender": "bot"})
    last_entity = extract_last_entity_from_history()

def extract_last_entity_from_history():
    global conversation_history
    for entry in reversed(conversation_history):
        if isinstance(entry, str) and entry.startswith("User:"):
            user_question = entry[6:].strip()
            doc = nlp(user_question)
            entities = [ent.text.lower() for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'GPE', 'LOC', 'PERSON']]
            if entities:
                return entities[-1]  # Get the most recent entity
    return None

def get_context():
    return "\n".join([f"{msg['sender']}: {msg['message']}" for msg in conversation_history])

def get_query_embedding(query):
    return model.encode(query, convert_to_tensor=True)

def resolve_coreferences(query):
    resolved_query = query
    doc = nlp(query)
    for token in doc:
        if token.pos_ == 'PRON':
            antecedent = None
            if token.text.lower() in ['it', 'they', 'this', 'there', 'these']:
                if last_entity:
                    resolved_query = resolved_query.replace(token.text, last_entity, 1)
            elif token.text.lower() in ['he', 'she']:
                antecedent = get_most_recent_entity('PERSON')
                if antecedent:
                    resolved_query = resolved_query.replace(token.text, antecedent, 1)
    return resolved_query

def get_most_recent_entity(label):
    if entity_history[label]:
        return entity_history[label][-1]
    return None

def find_best_answer(query, context):
    combined_query = query + " " + context
    query_embedding = get_query_embedding(combined_query)
    similarities = cosine_similarity([query_embedding], corpus_embeddings)
    best_match_index = np.argmax(similarities)
    best_similarity = similarities[0, best_match_index]

    if best_similarity > similarity_threshold:
        return corpus_answers[best_match_index], best_similarity
    return None, best_similarity

def find_best_entity_answer(entity):
    entity_related_qa_pairs = [
        qa for qa in qa_pairs if entity.lower() in qa['question'].lower() or entity.lower() in qa['answer'].lower()
    ]
    if entity_related_qa_pairs:
        # Find the most relevant question-answer pair based on the entity mention
        most_relevant_qa = max(entity_related_qa_pairs, key=lambda qa: (qa['question'].lower().count(entity.lower()), qa['answer'].lower().count(entity.lower())))
        return most_relevant_qa['answer']
    return "I'm not sure about that. Please contact the business directly for more information."


def handle_query_with_history(query):
    global last_entity
    if is_follow_up_query(query):
        if last_entity:
            follow_up_answer = find_best_entity_answer(last_entity)
            update_conversation_history(query, follow_up_answer)
            return follow_up_answer

    resolved_query = resolve_coreferences(query)
    context = get_context()
    answer, similarity = find_best_answer(resolved_query, context)

    if answer:
        response = answer
    else:
        response = "I'm not sure about that. Please contact the business directly for more information."
    update_conversation_history(query, response)
    return response

# Streamlit UI
st.set_page_config(page_title="Jessup Cellars Chatbot", page_icon=":wine_glass:", layout="wide")

st.markdown("""
    <style>
    .header { 
        background-color: #EDEBE7;
        padding: 10px;
        text-align: center;
        border-bottom: 1px solid #A9A193;
        font-family: 'Arial', sans-serif;
    }
    .footer { 
        background-color: #EDEBE7;
        padding: 10px;
        text-align: center;
        border-top: 1px solid #A9A193;
        position: fixed;
        bottom: 0;
        width: 100%;
        font-family: 'Arial', sans-serif;
    }
    .chat-container {
        height: 70vh;
        overflow-y: scroll;
        background-color: #DBD5CA;
        padding: 10px;
        border-radius: 10px;
        font-family: 'Arial', sans-serif;
    }
    .message {
        display: flex;
        padding: 5px;
        margin-bottom: 10px;
    }
    .user {
        justify-content: flex-end;
    }
    .bot {
        justify-content: flex-start;
    }
    .message-box {
        background-color: #DCf8C6;
        border-radius: 8px;
        padding: 10px;
        max-width: 70%;
        text-align: left;
        position: relative;
    }
    .bot .message-box {
        background-color: #F1F0F0;
    }
    .bubble {
        position: absolute;
        bottom: 0;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        box-shadow: 0 0 0 2px;
    }
    .user .bubble {
        background-color: #DCf8C6;
    }
    .bot .bubble {
        background-color: #F1F0F0;
    }
    .input-container {
        display: flex;
        align-items: center;
        margin-top: 10px;
    }
    .input-container input {
        flex: 1;
        padding: 10px;
        border-radius: 20px;
        border: 1px solid #A9A193;
        font-family: 'Arial', sans-serif;
    }
    .input-container button {
        background-color: #A9A193;
        color: #FFF;
        border: none;
        border-radius: 50%;
        padding: 10px;
        margin-left: 10px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header">
        <h1>Jessup Cellars Chatbot</h1>
    </div>
    """, unsafe_allow_html=True)

# Layout: Sidebar for UI Art
st.sidebar.image("https://jessupcellars.com/wp-content/uploads/2021/07/Jessup-Logo-400.png", use_column_width=True)  # Replace with your UI art URL
st.sidebar.title("Chat with Jessup Cellars Bot")
st.sidebar.text("Ask me anything about Jessup Cellars!")

# Main content
st.markdown("---")

# Chat area
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

def display_messages():
    # Display messages with user message first, followed by bot response
    for message in (st.session_state.conversation_history):
        bubble_class = 'user' if message['sender'] == 'user' else 'bot'
        st.markdown(f"""
            <div class="message {bubble_class}">
                <div class="message-box">
                    <strong>{'You' if message['sender'] == 'user' else 'Bot'}:</strong> {message['message']}
                </div>
            </div>
        """, unsafe_allow_html=True)

# Input box and send button
def main():
    user_message = st.text_input("", placeholder="Type your message here...", key="input_box")
    
    if st.button("Send"):
        if user_message:
            # Append user message first
            st.session_state.conversation_history.append({"message": user_message, "sender": "user"})

            bot_response = handle_query_with_history(user_message)
            
            # Append bot response
            st.session_state.conversation_history.append({"message": bot_response, "sender": "bot"})
    
    st.markdown("---")
    display_messages()
    
    # JavaScript to auto-scroll to bottom
    st.markdown("""
         <script>
        const chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        </script>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
    
# Footer
st.markdown("""
    <div class="footer">
        <p>© 2024 Jessup Cellars. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)