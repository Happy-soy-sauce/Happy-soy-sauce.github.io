<?php
// 读取 JSON 文件内容
$json = file_get_contents('./2.json');

// 解码 JSON 数据
$data = json_decode($json, true);

// 遍历数据并生成按钮
foreach ($data as $item) {
    $tags = $item['data'][0]['tags'];
    $originalUrl = $item['data'][0]['urls']['original'];

    // 生成按钮
    echo '<button>';
    echo implode(', ', $tags);
    echo '</button>';

    // 生成跳转链接
    echo '<a href="' . $originalUrl . '" target="_blank">' . $tags[0] . '</a>';
}
?>