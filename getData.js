const request = require('request');
const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const getStatement = i => {
	return new Promise((resolve, reject) => {
		var options = {
			'method': 'GET',
			'url': 'https://www.premier.vic.gov.au/site-4/statement-premier-' + i,
			'headers': {
			}
		};
		request(options, function (error, response) {
			if (error) console.log(error);
			if (response.statusCode == 404) {
				resolve(false);
			} else {
				let dom = new JSDOM(response.body);
				let lines = dom.window.document.querySelectorAll(".rpl-markup__inner p");
				let str = "";
				for (let i = 0; i < lines.length; i++) {
					if (typeof lines[i].textContent != "undefined" && lines[i].textContent != "undefined") {
						str += lines[i].textContent + "\n\n";
					}
				}
				resolve(str)
			}
		});
	})
}

const getStatementFromFile = file => {
	return new Promise((resolve, reject) => {
		fs.readFile(file, {}, (err, data) => {
			let dom = new JSDOM(data);
			let lines = dom.window.document.querySelectorAll(".rpl-markup__inner p");
			let str = "";
			for (let i = 0; i < lines.length; i++) {
				if (typeof lines[i].textContent != "undefined" && lines[i].textContent != "undefined") {
					str += lines[i].textContent + "\n\n";
				}
			}
			resolve(str)
		})
	})
}

const sleep = ms => {
	return new Promise((resolve, reject) => {
		setTimeout(resolve, ms)
	})
}

const init = async () => {
	for (let i = 1; i < 77; i++) {
		console.log(i)
		let statement = await getStatement(i);
		if (statement) {
			fs.writeFile('./statements/statement_' + i + '.txt', statement, async (err) => {
				if (err) {
					console.log(error);
				} else {
					console.log("File written");
				}
				await sleep(500);
			})
		}
	}
}
init();

// getStatement(67).then((statement) => {
// 	fs.writeFile('./statements/statement_' + 67 + '.txt', statement, (err) => {
// 		if (err) {
// 			console.log(error);
// 		} else {
// 			console.log("File written");
// 		}
// 	})
// })