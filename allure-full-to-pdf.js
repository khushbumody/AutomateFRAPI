const puppeteer = require("puppeteer");
const fs = require("fs");
const { PDFDocument } = require("pdf-lib");

const BASE_URL = "http://127.0.0.1:60643/"; // <-- CONFIRM PORT
const OUTPUT = "Allure-Full-Report.pdf";

const pages = [
  "#/",
  "#/suites",
  "#/behaviors",
  "#/packages",
  "#/timeline",
  "#/graphs"
];

(async () => {
  console.log("🚀 Starting Allure PDF generation...");

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });

  const page = await browser.newPage();
  let pdfFiles = [];

  for (let route of pages) {
    const url = BASE_URL + route;
    console.log("📄 Capturing:", url);

    // ✅ Correct navigation block
    await page.goto(url, { waitUntil: "domcontentloaded" });

    // wait until Allure UI loads
//    await page.waitForSelector("#app", { timeout: 15000 });
    //await page.goto(url, { waitUntil: "domcontentloaded" });
    await page.goto(url, { waitUntil: "networkidle2" });

// wait until at least one chart is visible
await page.waitForSelector("svg, canvas", { timeout: 20000 });

// extra wait for animations
await new Promise(resolve => setTimeout(resolve, 5000));

// wait for page to exist
await page.waitForSelector("body", { timeout: 15000 });


    // wait for charts/graphs
    await new Promise(resolve => setTimeout(resolve, 8000));

    // safe filename
    const safeName = route.replace(/[^a-zA-Z0-9]/g, "_");
    const file = `section${safeName}.pdf`;

    await page.pdf({
      path: file,
      format: "A4",
      landscape: true,
      printBackground: true,
      margin: {
        top: "20px",
        bottom: "20px",
        left: "10px",
        right: "10px"
      }
    });

    console.log("✅ PDF created:", file);
    pdfFiles.push(file);
  }

  // 🔀 Merge PDFs
  console.log("🔗 Merging PDFs...");
  const mergedPdf = await PDFDocument.create();

  for (const file of pdfFiles) {
    const pdfBytes = fs.readFileSync(file);
    const pdf = await PDFDocument.load(pdfBytes);
    const copiedPages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
    copiedPages.forEach(p => mergedPdf.addPage(p));
  }

  const finalPdf = await mergedPdf.save();
  fs.writeFileSync(OUTPUT, finalPdf);

  console.log("🎉 Full Allure report saved as:", OUTPUT);
  await browser.close();
})();
