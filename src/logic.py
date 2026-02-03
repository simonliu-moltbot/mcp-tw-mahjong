
import sys

def calculate_tai(
    melds, 
    eye, 
    hu_tile, 
    is_self_drawn, 
    is_dealer, 
    dealer_count, 
    wind_round, 
    wind_seat, 
    flower_tiles,
    is_concealed=False,
    wait_type="normal", # "normal", "edge" (edge/middle/single)
    is_last_tile=False,
    is_robbing_kong=False,
    is_kong_on_kong=False
):
    """
    Calculate Tai for Taiwan 16-card Mahjong (ATAWMJ Standard).
    melds: List of list of strings, e.g., [['1m','1m','1m'], ['2m','3m','4m'], ...]
    eye: List of 2 strings, e.g., ['5m', '5m']
    """
    total_tai = 0
    reasons = []

    # 1. 莊家相關
    if is_dealer:
        total_tai += 1
        reasons.append(f"莊家 (+1)")
        if dealer_count > 0:
            tai = dealer_count * 2
            total_tai += tai
            reasons.append(f"連 {dealer_count} 拉 {dealer_count} (+{tai})")
    
    # 2. 胡法相關 (ATAWMJ Rules)
    if is_self_drawn:
        if is_concealed:
            # 門清自摸 = 門清(1) + 自摸(1) + 門清自摸(1) = 3台
            total_tai += 3
            reasons.append("門清自摸 (+3)")
        else:
            total_tai += 1
            reasons.append("自摸 (+1)")
    elif is_concealed:
        total_tai += 1
        reasons.append("門清 (+1)")

    if wait_type == "edge":
        total_tai += 1
        reasons.append("邊/嵌/獨聽 (+1)")
    
    if is_robbing_kong:
        total_tai += 1
        reasons.append("搶槓 (+1)")
    
    if is_last_tile:
        total_tai += 1
        reasons.append("海底撈月 (+1)")

    # 3. 風牌與花牌
    winds = ['東', '南', '西', '北']
    wind_triplets = []
    for w in winds:
        if any(all(tile == w for tile in meld) for meld in melds):
            wind_triplets.append(w)
    
    # 四喜判定
    if len(wind_triplets) == 4:
        total_tai += 16
        reasons.append("大四喜 (+16)")
    elif len(wind_triplets) == 3:
        if any(all(tile == w for tile in eye) for w in winds if w not in wind_triplets):
            total_tai += 8
            reasons.append("小四喜 (+8)")
        else:
            # Not small four happiness, add individual winds
            for w in wind_triplets:
                if w == wind_round:
                    total_tai += 1
                    reasons.append(f"圈風 {w} (+1)")
                if w == wind_seat:
                    total_tai += 1
                    reasons.append(f"門風 {w} (+1)")
    else:
        # Normal wind counting
        for w in wind_triplets:
            if w == wind_round:
                total_tai += 1
                reasons.append(f"圈風 {w} (+1)")
            if w == wind_seat:
                total_tai += 1
                reasons.append(f"門風 {w} (+1)")
    
    # 三元牌
    dragons = {'中': '紅中', '發': '發財', '白': '白板'}
    dragon_triplets = []
    for d in dragons:
        if any(all(tile == d for tile in meld) for meld in melds):
            dragon_triplets.append(d)
    
    if len(dragon_triplets) == 3:
        total_tai += 8
        reasons.append("大三元 (+8)")
    elif len(dragon_triplets) == 2:
        if any(all(tile == d for tile in eye) for d in dragons if d not in dragon_triplets):
            total_tai += 4
            reasons.append("小三元 (+4)")
        else:
            for d in dragon_triplets:
                total_tai += 1
                reasons.append(f"{dragons[d]} (+1)")
    else:
        for d in dragon_triplets:
            total_tai += 1
            reasons.append(f"{dragons[d]} (+1)")

    # 花牌
    seat_to_flowers = {'東': ['f1', 'f5'], '南': ['f2', 'f6'], '西': ['f3', 'f7'], '北': ['f4', 'f8']}
    correct_flowers = seat_to_flowers.get(wind_seat, [])
    for f in flower_tiles:
        if f in correct_flowers:
            total_tai += 1
            reasons.append(f"正花 {f} (+1)")
    
    if len(flower_tiles) == 8:
        total_tai += 8
        reasons.append("八仙過海 (+8)")
    elif len(flower_tiles) == 7:
        total_tai += 8
        reasons.append("七搶一 (+8)")

    # 4. 牌型相關
    all_tiles = [t for m in melds for t in m] + eye
    
    # 清一色 / 湊一色
    suits = set()
    has_honor = False
    for t in all_tiles:
        if any(s in t for s in ['m', '萬']): suits.add('m')
        elif any(s in t for s in ['s', '條']): suits.add('s')
        elif any(s in t for s in ['p', '筒']): suits.add('p')
        else: has_honor = True
    
    if len(suits) == 1:
        if has_honor:
            total_tai += 2
            reasons.append("湊一色 (+2)")
        else:
            total_tai += 8
            reasons.append("清一色 (+8)")
    elif len(suits) == 0 and has_honor:
        total_tai += 16
        reasons.append("字一色 (+16)")

    # 碰碰胡
    triplet_count = sum(1 for meld in melds if len(meld) >= 3 and meld[0] == meld[1] == meld[2])
    if triplet_count >= 5:
        total_tai += 4
        reasons.append("碰碰胡 (+4)")

    return {
        "total_tai": total_tai,
        "reasons": reasons
    }
