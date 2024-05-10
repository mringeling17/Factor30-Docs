<!-- components/LineChart.svelte -->

<script lang="ts">
  import { onMount } from 'svelte';
  import ChartJS from 'chart.js/auto';

  // Define el tipo de datos para las entradas
  interface Entry {
    id: number;
    temperature: number;
    humidity: number;
    wind_speed: number;
    risk_level: string;
    uuid: string;
    received_at: string;
  }

  // Propiedad para los datos del gráfico
  export let data: Entry[];

  // Elemento canvas para el gráfico
  let canvas: HTMLCanvasElement;

  // Inicializa el gráfico al cargar el componente
  onMount(() => {
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Prepara los datos para el gráfico
    const labels = data.map((entry: Entry) => entry.received_at);
    const temperatures = data.map((entry: Entry) => entry.temperature);
    const humidities = data.map((entry: Entry) => entry.humidity);
    const windSpeeds = data.map((entry: Entry) => entry.wind_speed);

    // Configura el gráfico
    new ChartJS(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Temperatura',
            data: temperatures,
            borderColor: 'red',
            backgroundColor: 'transparent'
          },
          {
            label: 'Humedad',
            data: humidities,
            borderColor: 'blue',
            backgroundColor: 'transparent'
          },
          {
            label: 'Velocidad del Viento',
            data: windSpeeds,
            borderColor: 'green',
            backgroundColor: 'transparent'
          }
        ]
      },
      options: {
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'minute'
            }
          },
          y: {
            beginAtZero: true
          }
        }
      }
    });
  });
</script>

<canvas bind:this={canvas}></canvas>
