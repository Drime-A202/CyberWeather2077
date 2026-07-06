const CHINA_CITIES = [
    { name: '北京', province: '北京市', lat: 39.9042, lon: 116.4074 },
    { name: '上海', province: '上海市', lat: 31.2304, lon: 121.4737 },
    { name: '广州', province: '广东省', lat: 23.1291, lon: 113.2644 },
    { name: '深圳', province: '广东省', lat: 22.5431, lon: 114.0579 },
    { name: '成都', province: '四川省', lat: 30.5728, lon: 104.0668 },
    { name: '杭州', province: '浙江省', lat: 30.2741, lon: 120.1551 },
    { name: '西安', province: '陕西省', lat: 34.3416, lon: 108.9398 },
    { name: '重庆', province: '重庆市', lat: 29.4316, lon: 106.9123 },
    { name: '南京', province: '江苏省', lat: 32.0603, lon: 118.7969 },
    { name: '武汉', province: '湖北省', lat: 30.5928, lon: 114.3055 },
    { name: '青岛', province: '山东省', lat: 36.0671, lon: 120.3826 },
    { name: '天津', province: '天津市', lat: 39.3434, lon: 117.3616 },
    { name: '苏州', province: '江苏省', lat: 31.2989, lon: 120.5853 },
    { name: '厦门', province: '福建省', lat: 24.4798, lon: 118.0894 },
    { name: '哈尔滨', province: '黑龙江省', lat: 45.8038, lon: 126.5350 },
    { name: '长春', province: '吉林省', lat: 43.8171, lon: 125.3235 },
    { name: '沈阳', province: '辽宁省', lat: 41.8057, lon: 123.4315 },
    { name: '大连', province: '辽宁省', lat: 38.9140, lon: 121.6147 },
    { name: '济南', province: '山东省', lat: 36.6512, lon: 117.1201 },
    { name: '郑州', province: '河南省', lat: 34.7466, lon: 113.6254 },
    { name: '太原', province: '山西省', lat: 37.8706, lon: 112.5489 },
    { name: '石家庄', province: '河北省', lat: 38.0428, lon: 114.5149 },
    { name: '合肥', province: '安徽省', lat: 31.8206, lon: 117.2272 },
    { name: '南昌', province: '江西省', lat: 28.6820, lon: 115.8579 },
    { name: '长沙', province: '湖南省', lat: 28.2282, lon: 112.9388 },
    { name: '贵阳', province: '贵州省', lat: 26.6470, lon: 106.6302 },
    { name: '昆明', province: '云南省', lat: 25.0389, lon: 102.7183 },
    { name: '南宁', province: '广西壮族自治区', lat: 22.8170, lon: 108.3665 },
    { name: '海口', province: '海南省', lat: 20.0444, lon: 110.1993 },
    { name: '兰州', province: '甘肃省', lat: 36.0611, lon: 103.8343 },
    { name: '西宁', province: '青海省', lat: 36.6171, lon: 101.7778 },
    { name: '银川', province: '宁夏回族自治区', lat: 38.4872, lon: 106.2309 },
    { name: '乌鲁木齐', province: '新疆维吾尔自治区', lat: 43.8256, lon: 87.6168 },
    { name: '拉萨', province: '西藏自治区', lat: 29.6520, lon: 91.1721 },
    { name: '呼和浩特', province: '内蒙古自治区', lat: 40.8426, lon: 111.7490 },
    { name: '香港', province: '香港', lat: 22.3193, lon: 114.1694 },
    { name: '澳门', province: '澳门', lat: 22.1987, lon: 113.5439 },
    { name: '台北', province: '台湾省', lat: 25.0330, lon: 121.5654 },
    { name: '福州', province: '福建省', lat: 26.0745, lon: 119.2965 },
    { name: '温州', province: '浙江省', lat: 27.9938, lon: 120.6994 },
    { name: '宁波', province: '浙江省', lat: 29.8683, lon: 121.5440 },
    { name: '三亚', province: '海南省', lat: 18.2528, lon: 109.5119 },
];

const weatherCache = new Map();
const weatherCacheTime = new Map();
let chartInstance = null;
let currentWeather = window.initialWeather;
let activeCityName = '北京';
let weatherDataMap = {};

document.addEventListener('DOMContentLoaded', function() {
    initClock();
    initEChartsMap();
    initTooltip();
    if (currentWeather) {
        renderCityDetail(currentWeather);
    }
    fetchAllCitiesWeather();
    addLog('SYSTEM', '中国天气地图已激活');

    window.addEventListener('resize', function() {
        if (chartInstance) {
            chartInstance.resize();
        }
    });
});

function initClock() {
    const update = () => {
        const now = new Date();
        const h = String(now.getHours()).padStart(2, '0');
        const m = String(now.getMinutes()).padStart(2, '0');
        const s = String(now.getSeconds()).padStart(2, '0');
        const el = document.getElementById('current-time');
        if (el) el.textContent = `${h}:${m}:${s}`;
    };
    update();
    setInterval(update, 1000);
}

function initEChartsMap() {
    const chartDom = document.getElementById('china-map');
    if (!chartDom || !window.echarts) {
        addLog('ERROR', 'ECharts 库未加载');
        return;
    }

    chartInstance = echarts.init(chartDom, null, { renderer: 'canvas' });
    addLog('SYSTEM', '正在加载中国地图数据...');

    fetch('/static/data/china.json')
        .then(r => {
            if (!r.ok) throw new Error('地图数据加载失败');
            return r.json();
        })
        .then(geoJson => {
            echarts.registerMap('china', geoJson);
            addLog('SYSTEM', '中国地图数据已加载');
            renderEChartsMap();
        })
        .catch(err => {
            addLog('ERROR', '地图加载失败: ' + err.message);
        });
}

function renderEChartsMap() {
    const cityPoints = CHINA_CITIES.map(city => ({
        name: city.name,
        value: [city.lon, city.lat, 0]
    }));

    const option = {
        backgroundColor: 'transparent',
        tooltip: { show: false },
        geo: {
            map: 'china',
            roam: true,
            zoom: 1.2,
            center: [105, 36],
            scaleLimit: { min: 0.8, max: 5 },
            label: {
                show: true,
                color: 'rgba(0, 255, 242, 0.7)',
                fontSize: 10,
                fontFamily: 'Courier New, monospace'
            },
            itemStyle: {
                areaColor: 'rgba(10, 30, 60, 0.7)',
                borderColor: '#00fff2',
                borderWidth: 1,
                shadowColor: 'rgba(0, 255, 242, 0.5)',
                shadowBlur: 10
            },
            emphasis: {
                label: {
                    show: true,
                    color: '#fff',
                    fontSize: 12,
                    fontWeight: 'bold',
                    textShadowColor: '#00fff2',
                    textShadowBlur: 10
                },
                itemStyle: {
                    areaColor: 'rgba(0, 100, 150, 0.8)',
                    borderColor: '#00fff2',
                    borderWidth: 2,
                    shadowColor: 'rgba(0, 255, 242, 0.8)',
                    shadowBlur: 20
                }
            },
            select: {
                label: { show: true, color: '#ff00aa' },
                itemStyle: {
                    areaColor: 'rgba(100, 0, 80, 0.6)',
                    borderColor: '#ff00aa',
                    borderWidth: 2
                }
            },
            regions: []
        },
        series: [{
            name: '城市',
            type: 'effectScatter',
            coordinateSystem: 'geo',
            data: cityPoints.map(p => ({
                name: p.name,
                value: p.value,
                symbolSize: 10,
                itemStyle: {
                    color: '#00fff2',
                    shadowBlur: 10,
                    shadowColor: '#00fff2'
                }
            })),
            symbolSize: 10,
            showEffectOn: 'render',
            rippleEffect: { period: 4, scale: 3, brushType: 'stroke' },
            label: {
                show: true,
                position: 'right',
                formatter: '{b}',
                color: '#00fff2',
                fontSize: 11,
                fontFamily: 'Courier New, monospace',
                textShadowColor: '#000',
                textShadowBlur: 3
            },
            emphasis: {
                scale: 1.5,
                label: { show: true, color: '#fff', fontSize: 13, fontWeight: 'bold' },
                itemStyle: { color: '#ff00aa', shadowBlur: 20, shadowColor: '#ff00aa' }
            },
            zlevel: 2
        }]
    };

    chartInstance.setOption(option);

    chartInstance.on('mouseover', function(params) {
        if (params.componentType === 'series') {
            const cityName = params.name;
            const cityInfo = CHINA_CITIES.find(c => c.name === cityName);
            if (cityInfo) {
                showMapTooltip(cityInfo, params.event);
                updateCoords(cityInfo.lat, cityInfo.lon);
            }
        } else if (params.componentType === 'geo' && params.name) {
            const provinceName = params.name;
            const matchingCity = CHINA_CITIES.find(c => c.province.includes(provinceName) || provinceName.includes(c.province.split('省')[0].split('市')[0]));
            if (matchingCity) {
                showMapTooltip(matchingCity, params.event);
                updateCoords(matchingCity.lat, matchingCity.lon);
            }
        }
    });

    chartInstance.on('mouseout', function() { hideMapTooltip(); });

    chartInstance.on('click', function(params) {
        let cityInfo = null;
        if (params.componentType === 'series') {
            cityInfo = CHINA_CITIES.find(c => c.name === params.name);
        } else if (params.componentType === 'geo' && params.name) {
            const provinceName = params.name;
            cityInfo = CHINA_CITIES.find(c => c.province.includes(provinceName.split('省')[0].split('市')[0].split('自治区')[0]));
            if (!cityInfo) {
                cityInfo = CHINA_CITIES.find(c => provinceName.includes(c.name));
            }
        }
        if (cityInfo) {
            activeCityName = cityInfo.name;
            updateActiveCity(cityInfo.name);
            fetchCityWeather(cityInfo);
        }
    });

    addLog('SYSTEM', '中国地图渲染完成');
}

function initTooltip() {
}

function showMapTooltip(cityInfo, event) {
    const tooltip = document.getElementById('map-tooltip');
    const mapWrapper = document.getElementById('map-wrapper');
    if (!tooltip || !mapWrapper) return;

    document.getElementById('tooltip-city').textContent = cityInfo.name;
    document.getElementById('tooltip-code').textContent = '[LOADING]';
    document.getElementById('tooltip-temp').textContent = '--';
    document.getElementById('tooltip-desc').textContent = '同步中...';
    document.getElementById('tooltip-feels').textContent = '--';
    document.getElementById('tooltip-humidity').textContent = '--';
    document.getElementById('tooltip-wind').textContent = '--';
    document.getElementById('tooltip-loading').style.display = 'block';

    tooltip.style.display = 'block';
    tooltip.classList.add('tooltip-show');

    const rect = mapWrapper.getBoundingClientRect();
    const eventX = event.offsetX !== undefined ? event.offsetX : event.layerX;
    const eventY = event.offsetY !== undefined ? event.offsetY : event.layerY;

    let posX = event.clientX - rect.left + 15;
    let posY = event.clientY - rect.top + 15;

    const tooltipWidth = 220;
    const tooltipHeight = 180;

    if (posX + tooltipWidth > rect.width - 10) {
        posX = event.clientX - rect.left - tooltipWidth - 15;
    }
    if (posY + tooltipHeight > rect.height - 10) {
        posY = event.clientY - rect.top - tooltipHeight - 15;
    }
    if (posX < 10) posX = 10;
    if (posY < 10) posY = 10;

    tooltip.style.left = posX + 'px';
    tooltip.style.top = posY + 'px';

    const cacheKey = cityInfo.name;
    if (weatherCache.has(cacheKey) && (Date.now() - weatherCacheTime.get(cacheKey) < 600000)) {
        const cachedData = weatherCache.get(cacheKey);
        updateTooltipContent(cachedData);
        return;
    }

    fetchWeatherData(cityInfo);
}

function hideMapTooltip() {
    const tooltip = document.getElementById('map-tooltip');
    if (tooltip) {
        tooltip.style.display = 'none';
    }
}

function fetchWeatherData(cityInfo) {
    const cacheKey = cityInfo.name;
    const url = `/api/weather?lat=${cityInfo.lat}&lon=${cityInfo.lon}&name=${encodeURIComponent(cityInfo.name)}&country=CN`;

    addLog('NETWORK', `请求数据流: ${cityInfo.name}`);

    fetch(url)
        .then(r => {
            if (!r.ok) throw new Error('请求失败');
            return r.json();
        })
        .then(data => {
            weatherCache.set(cacheKey, data);
            weatherCacheTime.set(cacheKey, Date.now());
            weatherDataMap[cacheKey] = data;
            updateTooltipContent(data);
            updateMapMarkerColors();
            addLog('DATA', `${cityInfo.name} 数据流同步完成`);
        })
        .catch(err => {
            addLog('ERROR', `获取 ${cityInfo.name} 天气失败: ${err}`);
            const loading = document.getElementById('tooltip-loading');
            if (loading) loading.textContent = '> 数据同步失败';
        });
}

function fetchAllCitiesWeather() {
    addLog('SYSTEM', '开始批量获取城市天气数据...');
    const citiesToFetch = CHINA_CITIES.slice(0, 15);
    citiesToFetch.forEach((city, index) => {
        setTimeout(() => {
            if (!weatherCache.has(city.name)) {
                fetchWeatherData(city);
            }
        }, index * 300);
    });
}

function updateTooltipContent(data) {
    document.getElementById('tooltip-code').textContent = `[${data.current.cyber}]`;
    document.getElementById('tooltip-temp').textContent = data.current.temperature;
    document.getElementById('tooltip-desc').textContent = data.current.description;
    document.getElementById('tooltip-feels').textContent = data.current.feels_like;
    document.getElementById('tooltip-humidity').textContent = data.current.humidity;
    document.getElementById('tooltip-wind').textContent = data.current.wind_speed;
    document.getElementById('tooltip-loading').style.display = 'none';

    const tempColor = getTemperatureColor(data.current.temperature);
    const tooltipTemp = document.getElementById('tooltip-temp');
    if (tooltipTemp) tooltipTemp.style.color = tempColor;
}

function updateMapMarkerColors() {
    if (!chartInstance) return;

    const updatedData = CHINA_CITIES.map(city => {
        const data = weatherDataMap[city.name];
        const temp = data ? data.current.temperature : null;
        const color = temp !== null ? getTemperatureColor(temp) : '#00fff2';
        return {
            name: city.name,
            value: [city.lon, city.lat, temp || 0],
            symbolSize: temp !== null ? 12 : 10,
            itemStyle: {
                color: color,
                shadowBlur: 15,
                shadowColor: color
            }
        };
    });

    chartInstance.setOption({
        series: [{
            name: '城市',
            data: updatedData
        }]
    });
}

function getTemperatureColor(temp) {
    if (temp <= 0) return '#4a90ff';
    if (temp <= 15) return '#00d4ff';
    if (temp <= 25) return '#00ff88';
    if (temp <= 30) return '#ffcc00';
    return '#ff4444';
}

function updateCoords(lat, lon) {
    const latEl = document.getElementById('map-lat');
    const lonEl = document.getElementById('map-lon');
    if (latEl) latEl.textContent = lat.toFixed(4);
    if (lonEl) lonEl.textContent = lon.toFixed(4);
}

function updateActiveCity(name) {
    const el = document.getElementById('active-city');
    if (el) el.textContent = name;
}

function fetchCityWeather(cityInfo) {
    const cacheKey = cityInfo.name;
    if (weatherCache.has(cacheKey) && (Date.now() - weatherCacheTime.get(cacheKey) < 600000)) {
        renderCityDetail(weatherCache.get(cacheKey));
        return;
    }
    fetchWeatherData(cityInfo);
    const checkInterval = setInterval(() => {
        if (weatherCache.has(cacheKey)) {
            renderCityDetail(weatherCache.get(cacheKey));
            clearInterval(checkInterval);
        }
    }, 500);
    setTimeout(() => clearInterval(checkInterval), 10000);
}

function renderCityDetail(data) {
    if (!data || !data.current) return;
    const cur = data.current;

    document.getElementById('city-name').textContent = data.city;
    const metaItems = document.querySelectorAll('.city-meta .meta-item');
    if (metaItems[0]) metaItems[0].textContent = `[${data.country}]`;
    if (metaItems[1]) metaItems[1].textContent = `LAT: ${data.latitude.toFixed(4)}`;
    if (metaItems[2]) metaItems[2].textContent = `LON: ${data.longitude.toFixed(4)}`;

    document.getElementById('current-temp').textContent = cur.temperature;
    document.getElementById('current-desc').textContent = cur.description;
    document.querySelector('.temp-code').textContent = `[${cur.cyber}]`;

    const iconSymbol = document.getElementById('icon-symbol');
    const iconMap = {
        'sunny': '☀', 'partly-cloudy': '⛅', 'cloudy': '☁',
        'fog': '🌫', 'drizzle': '🌦', 'rain': '🌧',
        'snow': '❄', 'thunder': '⛈'
    };
    if (iconSymbol) iconSymbol.textContent = iconMap[cur.icon] || '☀';

    const elWind = document.getElementById('wind-speed');
    const elHum = document.getElementById('humidity');
    const elPres = document.getElementById('pressure');
    const elCloud = document.getElementById('cloud-cover');
    const elPrecip = document.getElementById('precip');
    const elUV = document.getElementById('uv-index');

    if (elWind) elWind.textContent = cur.wind_speed;
    if (elHum) elHum.textContent = cur.humidity;
    if (elPres) elPres.textContent = cur.pressure;
    if (elCloud) elCloud.textContent = cur.cloud_cover;
    if (elPrecip) elPrecip.textContent = cur.precipitation;
    if (elUV) elUV.textContent = data.uv_index;

    renderDaily(data.daily);
    applyWeatherTheme(cur.icon);

    const tempColor = getTemperatureColor(cur.temperature);
    const iconCore = document.getElementById('icon-core');
    if (iconCore) iconCore.setAttribute('stroke', tempColor);
}

function renderDaily(daily) {
    const list = document.getElementById('daily-list');
    if (!list || !daily) return;
    const iconMap = {
        'sunny': '☀', 'partly-cloudy': '⛅', 'cloudy': '☁',
        'fog': '🌫', 'drizzle': '🌦', 'rain': '🌧',
        'snow': '❄', 'thunder': '⛈'
    };
    list.innerHTML = daily.map(d => `
        <div class="daily-card-compact">
            <span class="daily-day">${d.day_name}</span>
            <span class="daily-icon">${iconMap[d.icon] || '☀'}</span>
            <span class="daily-temps"><span class="temp-hi">${d.temp_max}°</span>/${d.temp_min}°</span>
            <span class="daily-desc">${d.description}</span>
        </div>
    `).join('');
}

function applyWeatherTheme(icon) {
    const root = document.documentElement;
    let primary = '#00fff2';
    let secondary = '#ff00aa';

    if (icon === 'sunny') {
        primary = '#ffcc00'; secondary = '#ff6600';
    } else if (icon === 'cloudy' || icon === 'partly-cloudy') {
        primary = '#aacccc'; secondary = '#6688aa';
    } else if (icon === 'rain' || icon === 'drizzle') {
        primary = '#0099ff'; secondary = '#0055aa';
    } else if (icon === 'snow') {
        primary = '#bbddff'; secondary = '#88aacc';
    } else if (icon === 'thunder') {
        primary = '#aa00ff'; secondary = '#ff00aa';
    } else if (icon === 'fog') {
        primary = '#888899'; secondary = '#555566';
    }

    root.style.setProperty('--border-cyber', primary);
    root.style.setProperty('--accent-cyan', primary);
    root.style.setProperty('--accent-pink', secondary);
}

function addLog(tag, message) {
    const log = document.getElementById('system-log');
    if (!log) return;
    const now = new Date();
    const t = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
    const line = document.createElement('div');
    line.className = 'log-line';
    line.innerHTML = `<span class="log-time">[${tag} ${t}]</span> <span class="log-msg">${message}</span>`;
    log.appendChild(line);
    log.scrollTop = log.scrollHeight;
    while (log.children.length > 25) {
        log.removeChild(log.firstChild);
    }
}

setInterval(() => {
    addLog('SYSTEM', '数据缓存已刷新');
    weatherCache.clear();
    weatherCacheTime.clear();
}, 1800000);
