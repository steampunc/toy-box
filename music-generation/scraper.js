const puppeteer = require("puppeteer");
const cheerio = require("cheerio");
const fs = require("fs");


const url =  process.argv[2];

puppeteer
	.launch()
	.then(browser => browser.newPage())
	.then(page => {
		return page.goto(url).then(function() {
			return page.content();
		});
	})
	.then(html => {
		var filename = url.substring(url.lastIndexOf('/') + 1)
		fs.writeFileSync("scraper_files/" + filename + ".html", html, function (err) {
			if (err) throw err;
		});
	})
	.catch(console.error).then(() => process.exit(0));


