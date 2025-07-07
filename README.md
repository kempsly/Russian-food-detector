```markdown
# Проект: Распознавание блюд в ресторане с помощью YOLOv11

Данный проект реализует систему компьютерного зрения для детекции **8 видов блюд** в ресторанных видео с помощью нейросети **YOLOv11**. Проект охватывает весь ML-пайплайн: от обработки данных до обучения и визуализации результатов.

---

## Структура проекта

```

russian-yolo-food-detection/
├── data/
│   ├── videos/                   # Исходные видеофайлы
│   ├── frames/                   # Извлечённые кадры
│   ├── all\_frames\_keep/          # Очищенные уникальные кадры
│   ├── data\_to\_augment/          # Аннотированные изображения
│   ├── augmented/                # Аугментированные изображения и метки
│   ├── dataset/                  # Финальное разбиение на train/val/test
│   └── predicted\_videos/         # Результаты предсказаний на видео
├── notebooks/
│   └── research.ipynb            # Все этапы проекта
├── report/
│   └── final\_report.md           # Финальный отчёт
├── runs/                        # Логи обучения, веса моделей
├── src/                         # Все Python-скрипты
├── food\_dataset.yaml            # Конфигурация датасета
├── requirements.txt             # Зависимости
└── README.md                    # Описание проекта

````

---

## Установка и зависимости

1. Установите Miniconda и создайте виртуальное окружение:

```bash
conda create -n yolovenv python=3.8
conda activate yolovenv
pip install -r requirements.txt
````

2. Основные зависимости:

* `ultralytics>=8.3`
* `albumentations`
* `opencv-python`
* `pyyaml`, `matplotlib`, `numpy`

3. **Предобученные веса `yolov11x.pt` нужно скачать вручную:**

[Ссылка для скачивания](https://docs.ultralytics.com/models/yolo11/#supported-tasks-and-modes)

---

## Датасет

* 8 классов блюд
* Ручная аннотация через [MakeSense.ai](https://www.makesense.ai)
* Аугментация с помощью `Albumentations`
* Деление: 70% — train, 20% — val, 10% — test

Конфигурация `food_dataset.yaml`:

```yaml
path: data/dataset
train: images/train
val: images/val
test: images/test
nc: 8
names:
  0: daikon_salad
  1: greek_salad
  2: shashlik
  3: wrap
  4: green_tea
  5: Borscht
  6: cheese_soup
  7: fondue
```

---

## Обучение модели

### Первая итерация

```python
results = model.train(
    data='dataset/food_dataset.yaml',
    epochs=50,
    imgsz=640,
    batch=8,
    lr0=0.01,
    project="runs/detect",
    name="iter1",
    device=[0, 1],
    plots=True
)
```

Метрики (на тесте):

* Precision: **0.985**
* Recall: **1.000**
* mAP\@0.5: **0.995**
* mAP\@0.5:0.95: **0.915**
* F1 Score: **0.992**

---

### Вторая итерация (тюнинг)

```python
results = model.train(
    data='dataset/food_dataset.yaml',
    epochs=70,
    imgsz=640,
    batch=8,
    lr0=0.005,
    project="runs/detect",
    name="iter2",
    device=0,
    plots=True
)
```

Метрики (на тесте):

* Precision: **0.978**
* Recall: **1.000**
* mAP\@0.5: **0.995**
* mAP\@0.5:0.95: **0.918**
* F1 Score: **0.989**

---

## Визуализация

YOLO автоматически сохраняет графики:

* `runs/detect/iter1/results.png`
* `runs/detect/iter2/results.png`

Графики включают:

* Loss (classification, box)
* mAP
* Precision / Recall

---

## 🎥 Предсказания на видео

Пример кода для запуска предсказаний на видео с сохранением результатов:

```python
from ultralytics import YOLO
import os

model = YOLO('runs/detect/iter1/weights/best.pt')
video_dir = 'data/videos'
output_dir = 'data/predicted_videos'
video_files = ['1.mov', '2_1.mov', '3_1.mov', '3_2.mov', '4.mov', '4_1.mov']
os.makedirs(output_dir, exist_ok=True)

for video_name in video_files:
    video_path = os.path.join(video_dir, video_name)
    if not os.path.isfile(video_path):
        continue
    model.predict(
        source=video_path,
        save=True,
        save_txt=False,
        save_conf=True,
        project=output_dir,
        name=os.path.splitext(video_name)[0],
        exist_ok=True
    )
```

---

### Пример предсказания

📽️ [Посмотреть видео с предсказанием `3_1.mov`](data/predicted_videos/3_1/3_1.avi)

## 🎥 Видео с предсказаниями

Ниже представлены ссылки на все 6 видео с прорисованными bounding boxes:

- [Видео 1](https://amlstorageblobstore.blob.core.windows.net/amlcontainerblob00/predicted-videos/1.avi)
- [Видео 2_1](https://amlstorageblobstore.blob.core.windows.net/amlcontainerblob00/predicted-videos/2_1.avi)
- [Видео 3_1](https://amlstorageblobstore.blob.core.windows.net/amlcontainerblob00/predicted-videos/3_1.avi)
- [Видео 3_2](https://amlstorageblobstore.blob.core.windows.net/amlcontainerblob00/predicted-videos/3_2.avi)
- [Видео 4](https://amlstorageblobstore.blob.core.windows.net/amlcontainerblob00/predicted-videos/4.avi)
- [Видео 4_1](https://amlstorageblobstore.blob.core.windows.net/amlcontainerblob00/predicted-videos/4_1.avi)

Чтобы посмотреть, кликните по ссылке — видео откроется или скачается.

---

Видео сохранено в формате AVI с прорисованными bounding boxes.

---

## Данные и модели

Для удобства загрузки больших файлов размещены на Google Drive:

* 📂 [Датасет (кадры и аннотации)](https://drive.google.com/drive/folders/your-folder-id)
* 📂 [Обученные модели](https://drive.google.com/drive/folders/your-model-folder-id)
* 📂 [Видео для предсказаний](https://drive.google.com/drive/folders/your-video-folder-id)

---

## Как воспроизвести

1. Клонируйте репозиторий
2. Создайте и активируйте виртуальное окружение
3. Скачайте `yolov11x.pt` и все файлы с Google Drive
4. Запустите `notebooks/research.ipynb`, который включает:

   * извлечение кадров
   * аугментацию
   * обучение
   * предсказания
   * визуализацию

---

## Время, затраченное на выполнение

| Этап                   | Время          |
| ---------------------- | -------------- |
| Подготовка и аннотация | \~6 часов      |
| Аугментация и разметка | \~3 часа       |
| Обучение               | \~5 часов      |
| Анализ и визуализация  | \~2 часа       |
| Документация           | \~2 часа       |
| **Итого**              | **\~18 часов** |

---

## Итог

Модель показала высокое качество распознавания на тестовых данных. Проект структурирован, легко воспроизводим, снабжён визуализациями и предсказаниями.

---

🔗 [Документация YOLOv11](https://docs.ultralytics.com/models/yolo11/)

```