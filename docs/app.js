// 公租房监控页面 - 主脚本

// 全局状态
let allHouses = [];
let filters = {};
let enabledFilters = [];

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成，初始化数据...');
    loadDashboardData();
});

// 加载仪表板数据
async function loadDashboardData() {
    try {
        // 加载今日数据
        const todayResponse = await fetch('./data/today.json');
        const todayData = await todayResponse.json();

        // 加载筛选配置
        const filtersResponse = await fetch('./data/filters.json');
        const filtersData = await filtersResponse.json();

        // 更新全局状态
        allHouses = todayData.houses || [];
        filters = filtersData.all_filters || {};
        enabledFilters = filtersData.enabled_filters || [];

        console.log('数据加载成功:', {
            houses: allHouses.length,
            filters: enabledFilters.length
        });

        // 更新页面
        updateStats(todayData);
        renderFilters(filtersData.filter_stats);
        renderHouses(allHouses);
        updateTimestamp(todayData);

    } catch (error) {
        console.error('数据加载失败:', error);
        showError('数据加载失败，请稍后刷新页面');
    }
}

// 更新统计卡片
function updateStats(data) {
    document.getElementById('total-count').textContent = data.total_count || 0;
    document.getElementById('filtered-count').textContent = data.filtered_count || 0;
    document.getElementById('new-count').textContent = data.new_count || 0;
    document.getElementById('avg-price').textContent = data.avg_price || 0;
}

// 渲染筛选按钮
function renderFilters(filterStats) {
    const container = document.getElementById('filters-container');
    if (!container) return;

    if (!filterStats || filterStats.length === 0) {
        container.innerHTML = '<p class="no-filters">暂无筛选条件</p>';
        return;
    }

    container.innerHTML = filterStats.map(filter => `
        <div class="filter-item">
            <button class="filter-btn ${filter.enabled ? 'active' : ''}"
                    onclick="toggleFilter('${filter.name}')"
                    data-filter="${filter.name}">
                <span class="filter-name">${filter.name}</span>
                <span class="filter-count">${filter.count}套</span>
            </button>
            <p class="filter-desc">${filter.description || ''}</p>
        </div>
    `).join('');
}

// 渲染房源列表
function renderHouses(houses) {
    const container = document.getElementById('houses-container');
    if (!container) return;

    if (!houses || houses.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>暂无房源数据</p></div>';
        return;
    }

    container.innerHTML = houses.map((house, index) => `
        <div class="house-card" data-rent="${house.rent_value || 0}">
            <div class="house-header">
                <h3 class="house-name">${house.house_name || '未知房源'}</h3>
                <span class="house-rent">¥${house.rent || 0}/月</span>
            </div>
            <div class="house-details">
                <div class="detail-item">
                    <span class="label">区域</span>
                    <span class="value">${house.house_site || '未知'}</span>
                </div>
                <div class="detail-item">
                    <span class="label">户型</span>
                    <span class="value">${house.house_type || '未知'}</span>
                </div>
                <div class="detail-item">
                    <span class="label">楼层</span>
                    <span class="value">${house.floor || '未知'}</span>
                </div>
                <div class="detail-item">
                    <span class="label">面积</span>
                    <span class="value">${house.area || '未知'}㎡</span>
                </div>
            </div>
            ${house.matched_filters && house.matched_filters.length > 0 ? `
                <div class="house-filters">
                    <span class="filter-tag">${house.matched_filters.join('、')}</span>
                </div>
            ` : ''}
        </div>
    `).join('');
}

// 更新时间戳
function updateTimestamp(data) {
    const timestamp = document.getElementById('update-time');
    if (timestamp && data.update_time) {
        const date = new Date(data.update_time);
        const formatted = date.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
        timestamp.textContent = `更新时间: ${formatted}`;
    }
}

// 切换筛选条件
function toggleFilter(filterName) {
    const btn = document.querySelector(`[data-filter="${filterName}"]`);
    if (btn) {
        btn.classList.toggle('active');
    }

    applyFilters();
}

// 应用筛选
function applyFilters() {
    const activeFilters = document.querySelectorAll('.filter-btn.active');
    const activeNames = Array.from(activeFilters).map(btn => btn.dataset.filter);

    let filtered = allHouses;

    if (activeNames.length > 0) {
        filtered = allHouses.filter(house => {
            return house.matched_filters &&
                   house.matched_filters.some(f => activeNames.includes(f));
        });
    }

    renderHouses(filtered);
    updateFilteredCount(filtered.length);
}

// 更新筛选后数量
function updateFilteredCount(count) {
    const countEl = document.getElementById('filtered-count');
    if (countEl) {
        countEl.textContent = count;
    }
}

// 显示错误信息
function showError(message) {
    const container = document.getElementById('main-content');
    if (container) {
        container.innerHTML = `
            <div class="error-state">
                <div class="error-icon">⚠️</div>
                <h2>出错了</h2>
                <p>${message}</p>
                <button onclick="location.reload()" class="reload-btn">刷新页面</button>
            </div>
        `;
    }
}

// 排序功能
function sortHouses(field) {
    allHouses.sort((a, b) => {
        if (field === 'rent') {
            return (a.rent_value || 0) - (b.rent_value || 0);
        }
        return 0;
    });
    renderHouses(allHouses);
}
