#!/bin/bash

echo "Content-Type:text/html;charset=utf-8"
echo ""

/bin/cat << EOM
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Visca el Valencia CF</title>

<style>
body {
  margin: 20px;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: #0f172a;
  text-align: center;
}

h1 {
  color: #e11d48;
  margin-bottom: 20px;
}

.contenedor {
  background: linear-gradient(135deg, #0f172a, #1e293b);
  border-radius: 16px;
  padding: 30px;
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0 10px 25px rgba(0,0,0,0.12);
}

.imagenes {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 25px 0;
  flex-wrap: wrap;
}

.imagenes img {
  max-width: 180px;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.2);
  transition: transform 0.25s ease;
}

.imagenes img:hover {
  transform: scale(1.05);
}

button {
  padding: 10px 22px;
  border: none;
  border-radius: 10px;
  background: #2563eb;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.3s ease;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

button:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 8px 18px rgba(0,0,0,0.3);
}
</style>

<script>
function nuevo(){
  window.location.href = "/cgi-bin/info.cgi";
}
</script>

</head>

<body>

  <div class="contenedor">
    <h1>Visca el Valencia Club de Fútbol</h1>

    <div class="imagenes">
      <img src="https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/94.png" alt="Escudo Valencia CF">
      <img src="https://fotografias.lasexta.com/clipping/cmsimages02/2021/05/08/307FADD0-8E60-4C85-B9D0-01F721B6BF3F/104.jpg?crop=766,766,x250,y0&width=1200&height=1200&optimize=low&format=webply" alt="Peter Lim">
    </div>

    <button onclick="nuevo()">Volver a Inicio</button>
  </div>

</body>
</html>
EOM
