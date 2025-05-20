# Alonhadat
## Fields
address	area bedrooms date floors price	title url

## Field Descriptions and Processing:
*   `address`: (string) Textual address.
    *   *Expected processing*: Parse to extract components like street, ward, district, and city.
*   `area`: (string) Area of the property, includes " m2".
    *   *Expected processing*: Remove " m2" suffix, convert to a numerical type (float). Handle potential missing values.
*   `bedrooms`: (string) Number of bedrooms, includes " phòng ngủ".
    *   *Expected processing*: Remove " phòng ngủ" suffix, convert to an integer. Handle cases with no bedroom information or non-numeric values.
*   `date`: (string) Posting date, can be relative like "Hôm nay".
    *   *Expected processing*: Convert to datetime objects. "Hôm nay" should be resolved to the current date.
*   `floors`: (string) Number of floors, includes " lầu".
    *   *Expected processing*: Remove " lầu" suffix, convert to an integer. Handle cases with no floor information or non-numeric values.
*   `price`: (string) Price of the property, includes units like " tỷ".
    *   *Expected processing*: Parse to extract numerical value and unit (e.g., tỷ, triệu). Convert to a consistent numerical unit (e.g., VND). Handle cases like "Thỏa thuận" (negotiable price).
*   `title`: (string) Title of the listing.
    *   *Expected processing*: Generally, keep as is for textual analysis or feature extraction (e.g., using NLP techniques).
*   `url`: (string) URL of the listing.
    *   *Expected processing*: Keep as is, useful as a unique identifier or for accessing the original listing.

# Batdongsan
## Fields
"Diện tích","Hướng ban công","Hướng nhà","Mặt tiền","Mức giá","Mức giá internet","Mức giá nước","Mức giá điện","Nội thất","Pháp lý","Số phòng ngủ","Số phòng tắm, vệ sinh","Số tầng","Thời gian dự kiến vào ở","Tiện ích","title","url","Đường vào"

## Field Descriptions and Processing:
*   `Diện tích`: (string) Area, includes " m²".
    *   *Expected processing*: Remove " m²" suffix, convert to float. Handle missing values.
*   `Hướng ban công`: (string) Balcony direction (e.g., "Đông - Nam").
    *   *Expected processing*: Categorical feature. May need encoding (e.g., one-hot encoding) if used in a model. Handle missing values.
*   `Hướng nhà`: (string) House direction (e.g., "Bắc").
    *   *Expected processing*: Categorical feature. May need encoding. Handle missing values.
*   `Mặt tiền`: (string) Frontage width, may include " m".
    *   *Expected processing*: Remove " m" suffix if present, convert to float. Handle missing or non-numeric values.
*   `Mức giá`: (string) Price, can be "Thỏa thuận" or include units like "tỷ", "triệu/tháng".
    *   *Expected processing*: Complex parsing needed. Identify if it's a sale price or rental price (per month). Convert to a consistent numerical unit. Handle "Thỏa thuận".
*   `Mức giá internet`, `Mức giá nước`, `Mức giá điện`: (string) Utility prices.
    *   *Expected processing*: Investigate typical values. Convert to numerical if applicable, or treat as categorical. Handle missing values.
*   `Nội thất`: (string) Furniture status (e.g., "Đầy đủ", "Cơ bản").
    *   *Expected processing*: Categorical feature. May need encoding. Handle missing values.
*   `Pháp lý`: (string) Legal status (e.g., "Sổ đỏ/ Sổ hồng", "Hợp đồng mua bán").
    *   *Expected processing*: Categorical feature. May need encoding. Handle missing values.
*   `Số phòng ngủ`: (string) Number of bedrooms, includes " phòng".
    *   *Expected processing*: Remove " phòng" suffix, convert to integer. Handle missing values.
*   `Số phòng tắm, vệ sinh`: (string) Number of bathrooms, includes " phòng".
    *   *Expected processing*: Remove " phòng" suffix, convert to integer. Handle missing values.
*   `Số tầng`: (string) Number of floors, may include " tầng".
    *   *Expected processing*: Remove " tầng" suffix if present, convert to integer. Handle missing values.
*   `Thời gian dự kiến vào ở`: (string) Expected availability time.
    *   *Expected processing*: Parse into a date or a relative duration if possible. Handle missing values.
*   `Tiện ích`: (string) Amenities.
    *   *Expected processing*: Potentially a list of items. May need parsing (e.g., splitting by comma) and then techniques like one-hot encoding for each amenity if used in modeling. Handle missing values.
*   `title`: (string) Title of the listing.
    *   *Expected processing*: Keep as is for textual analysis or feature extraction.
*   `url`: (string) URL of the listing.
    *   *Expected processing*: Keep as is.
*   `Đường vào`: (string) Access road width, may include " m".
    *   *Expected processing*: Remove " m" suffix if present, convert to float. Handle missing values.

# Nhatot
## Fields
"Description","Location","Price","Price per m²","Space","Title"

## Field Descriptions and Processing:
*   `Description`: (string) Contains details like number of bedrooms (PN), property type (e.g., "Nhà ngõ, hẻm").
    *   *Expected processing*: Parse to extract number of bedrooms and property type. Convert number of bedrooms to integer. Property type is categorical.
*   `Location`: (string) Location information, includes district and relative time (e.g., "Quận Thanh Xuân • 2 ngày trước").
    *   *Expected processing*: Parse to extract district and posting date. Convert posting date to datetime objects.
*   `Price`: (string) Price of the property, includes units like " tỷ".
    *   *Expected processing*: Parse to extract numerical value and unit. Convert to a consistent numerical unit (e.g., VND).
*   `Price per m²`: (string) Price per square meter, includes units like " tr/m²".
    *   *Expected processing*: Remove " tr/m²" suffix, convert to a numerical type (float). Handle potential missing values.
*   `Space`: (string) Area of the property, includes " m²".
    *   *Expected processing*: Remove " m²" suffix, convert to a numerical type (float). Handle potential missing values.
*   `Title`: (string) Title of the listing.
    *   *Expected processing*: Keep as is for textual analysis or feature extraction.
