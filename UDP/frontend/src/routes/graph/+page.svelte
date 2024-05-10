<script lang="ts">
	import { onMount } from 'svelte';
	import Chart from 'chart.js/auto';

	interface Measurement {
		temperature: number;
		humidity: number;
		wind_speed: number;
		received_at: string;
	}

	let currentTemperature = 0;
	let currentHumidity = 0;
	let currentWindSpeed = 0;
	let data: Measurement[] = [];
	let chart: Chart<'line', number[], string> | null = null;
	let canvasElement: HTMLCanvasElement;

	onMount(async () => {
		await fetchData();
		const interval = setInterval(fetchData, 5000);
	});

	async function fetchData() {
		try {
			console.log('Fetching Data');
			const response = await fetch('http://192.168.1.118:5000/recent_measurements');
			if (!response.ok) {
				throw new Error('Error al obtener las mediciones');
			}
			const rawData: Measurement[] = await response.json();
			data = rawData
				.filter((d) => d.temperature <= 200 && d.humidity <= 200 && d.wind_speed <= 200)
				.sort((a, b) => new Date(a.received_at).getTime() - new Date(b.received_at).getTime());
			if (data.length > 0) {
				const latestData = data[data.length - 1];
				currentTemperature = latestData.temperature;
				currentTemperature = Math.round(currentTemperature * 100) / 100;

				currentHumidity = latestData.humidity;
				currentHumidity = Math.round(currentHumidity * 100) / 100;

				currentWindSpeed = latestData.wind_speed;
				currentWindSpeed = Math.round(currentWindSpeed * 100) / 100;
			}
			if (canvasElement) {
				updateChart();
			}
		} catch (e) {
			console.log(`Error al cargar los datos: ${e}`);
		}
	}

	function formatDate(dateStr: string): string {
		const utcDate = new Date(dateStr); // Suponiendo que dateStr está en UTC
		const gmt4Offset = utcDate.getTime() - utcDate.getTimezoneOffset() * 60000 - 4 * 3600000; // Restar 4 horas en milisegundos para GMT-4
		const gmt4Date = new Date(gmt4Offset);

		// Usar slice() en lugar de substr()
		return gmt4Date.toISOString().slice(11, 19); // Obtener la hora en formato hh:mm:ss
	}

	function updateChart() {
		console.log('Updating chart...');
		const ctx = canvasElement.getContext('2d');
		if (ctx && chart) {
			console.log('Updating existing chart...');
			chart.data.labels = data.map((d) => formatDate(d.received_at));
			chart.data.datasets.forEach((dataset, index) => {
				switch (index) {
					case 0:
						dataset.data = data.map((d) => d.temperature);
						break;
					case 1:
						dataset.data = data.map((d) => d.humidity);
						break;
					case 2:
						dataset.data = data.map((d) => d.wind_speed);
						break;
				}
			});
			chart.update();
		} else if (ctx) {
			console.log('Creating new chart...');
			chart = new Chart(ctx, {
				type: 'line',
				data: {
					labels: data.map((d) => formatDate(d.received_at)),
					datasets: [
						{
							label: 'Temperatura (°C)',
							data: data.map((d) => d.temperature),
							borderColor: 'rgb(255, 99, 132)',
							backgroundColor: 'rgba(255, 99, 132, 0.5)',
							fill: false
						},
						{
							label: 'Humedad (%)',
							data: data.map((d) => d.humidity),
							borderColor: 'rgb(54, 162, 235)',
							backgroundColor: 'rgba(54, 162, 235, 0.5)',
							fill: false
						},
						{
							label: 'Velocidad del Viento (m/s)',
							data: data.map((d) => d.wind_speed),
							borderColor: 'rgb(75, 192, 192)',
							backgroundColor: 'rgba(75, 192, 192, 0.5)',
							fill: false
						}
					]
				},
				options: {
					scales: {
						y: {
							beginAtZero: true
						}
					}
				}
			});
		} else {
			console.log('No se pudo obtener el contexto del canvas');
		}
	}

	function padTo2Digits(num: number) {
		return num.toString().padStart(2, '0');
	}
</script>

<div style="display: flex; justify-content: space-around; padding-bottom: 20px;">
	<div>Temperatura Actual: {currentTemperature} °C</div>
	<div>Humedad Actual: {currentHumidity} %</div>
	<div>Velocidad del Viento Actual: {currentWindSpeed} m/s</div>
</div>

<canvas bind:this={canvasElement} width="800" height="400"></canvas>

{#if data.length === 0}
	<p>No se han recibido datos aún.</p>
{/if}
