import requests
import json

# UID 입력받기
def get_user_uid():
    uid = input("UID를 입력하세요: ")
    return uid

# Enka.Network API에서 데이터를 가져오는 함수
def fetch_player_data(uid):
    url = f"https://enka.network/api/uid/{uid}"
    headers = {
        "User-Agent": "GenshinArtifactCalculator/1.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# 전시된 캐릭터들의 avatarId를 리스트로 저장하는 함수
def get_avatar_id_list(player_data):
    avatar_list = []
    show_avatar_info = player_data.get('playerInfo', {}).get('showAvatarInfoList', [])
    for avatar in show_avatar_info:
        avatar_id = avatar.get('avatarId')
        avatar_list.append(avatar_id)
    return avatar_list

# JSON 파일 불러오기
def load_json_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# avatarId와 featureTagGroupID가 일치하는 부분에서 iconName 값에서 UI_AvatarIcon_ 부분을 제거하여 저장하는 함수
def get_icon_names_by_avatar_id(data, avatar_ids):
    icon_names = []
    for avatar_id in avatar_ids:
        for entry in data:
            if entry.get('featureTagGroupID') == avatar_id:
                icon_name = entry.get('iconName', "")
                clean_icon_name = icon_name.replace("UI_AvatarIcon_", "")
                icon_names.append(clean_icon_name)
                break
    return icon_names

# 특정 캐릭터의 성유물 정보 출력 함수
def print_artifact_info(character_data):
    equip_list = character_data.get("equipList", [])
    for equip in equip_list:
        if equip.get("flat", {}).get("itemType") == "ITEM_RELIQUARY":  # 성유물인지 확인
            equip_type = equip["flat"].get("equipType", "Unknown")
            print(f"성유물 타입: {equip_type}")
            
            main_stat = equip["reliquaryMainstat"]
            print(f"  주 옵션: {main_stat['mainPropId']} +{main_stat['statValue']}")
            
            sub_stats = equip["reliquarySubstats"]
            for sub in sub_stats:
                print(f"  부 옵션: {sub['appendPropId']} +{sub['statValue']}")

def main():
    # 1. 사용자에게 UID 입력받기
    uid = get_user_uid()

    # 2. 입력받은 UID로 API에서 데이터 가져오기
    player_data = fetch_player_data(uid)
    if not player_data:
        return

    # 3. 전시된 캐릭터들의 avatarId 리스트로 저장
    avatar_id_list = get_avatar_id_list(player_data)
    
    if len(avatar_id_list) == 0:
        print("전시된 캐릭터가 없습니다.")
        return

    # 4. JSON 파일 URL (Gitlab URL)
    json_url = "https://gitlab.com/Dimbreath/AnimeGameData/-/raw/master/ExcelBinOutput/AvatarExcelConfigData.json"
    
    # 5. JSON 데이터 로드
    json_data = load_json_from_url(json_url)
    if not json_data:
        return

    # 6. avatarId와 일치하는 iconName 목록 가져오기
    icon_names = get_icon_names_by_avatar_id(json_data, avatar_id_list)

    # 7. 캐릭터 리스트 번호 출력
    print("\n--- 캐릭터 목록 ---")
    for idx, icon_name in enumerate(icon_names, 1):
        print(f"{idx}. {icon_name}")

    # 8. 사용자에게 캐릭터 선택받기
    selected_idx = int(input("성유물 정보를 확인할 캐릭터 번호를 선택하세요: ")) - 1
    if selected_idx < 0 or selected_idx >= len(avatar_id_list):
        print("잘못된 번호입니다.")
        return

    # 9. 선택한 캐릭터의 avatarId로 성유물 정보 가져오기
    avatar_info_list = player_data.get("avatarInfoList", [])
    selected_avatar_id = avatar_id_list[selected_idx]

    # 10. 선택된 캐릭터의 성유물 정보 출력
    for character in avatar_info_list:
        if character.get("avatarId") == selected_avatar_id:
            print_artifact_info(character)
            break

if __name__ == "__main__":
    main()