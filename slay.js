const links = [
    "http://127.0.0.1:5000/run/game1.py",
    "http://127.0.0.1:5000/run/gridart/gridart/GridArt.py",
];


let rotation = 0;


document.getElementById("randomBtn").addEventListener("click", function() {


    rotation += 360 * 5 + Math.random() * 360;
    document.getElementById("wheel").style.transform = `rotate(${rotation}deg)`;


    setTimeout(() => {
        const randomLink = links[Math.floor(Math.random() * links.length)];
        window.location.href = randomLink;
    }, 4000);
});

// wheel

const wheel = document.getElementById("wheel");
const randomBtn = document.getElementById("randomBtn");
const rotationValues = [
    { minDegree: 0, maxDegree: 90, value: 1 },
    { minDegree: 91, maxDegree: 180, value: 2 },
    { minDegree: 181, maxDegree: 270, value: 3 },
    { minDegree: 271, maxDegree: 360, value: 4 },
];

const data = [16, 16, 16, 16];
var pieColors = [
    "#003366",
    "#003F7D",
    "#FF8E00",
    "#FD7702",
];

let myChart = new Chart(wheel, {
    plugins: [ChartDataLabels],
    type: "pie",
    data: {
        labels: [1, 2, 3, 4],
        datasets: [
            {
                backgroundColor: pieColors,
                data: data, 
            },
        ],
    },
    options: {
        responsive: true,
        animation: { duration: 0},
        plugins: {
            tooltip: false,
            legend: {
                display: false,
            },
            datalabels: {
                color: "#ffffff",
                formatter: (_, context) => context.chart.data.labels[context.dataIndex],
                font: { size: 24 },
            },
        },
    },
});

let count = 0;
let resultValue = 101;
randomBtn.addEventListener("click", () => {
    randomBtn.disabled = true;
    let randomDegree = Math.floor(Math.random() * (355 - 0 + 1) + 0);
    let rotationInterval = window.setInterval(() => {
        myChart.options.rotation = myChart.options.rotation + resultValue;
        myChart.update();
        if (myChart.options.rotation >= 360) {
            count += 1;
            resultValue -= 5;
            myChart.options.rotation = 0;
        } else if (count > 15 && myChart.options.rotation == randomDegree) {
            valueGenerator(randomDegree);
            clearInterval(rotationInterval);
            count = 0;
            resultValue = 101;
        }
    }, 10); 
});
