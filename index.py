import requests
from openstep_plist import loads
import base64


def main():

    ### Set these

    REPO_OWNER_NAME = "org-or-username"
    REPO_NAME = "repo-name"
    GLYPHSPACKAGE_PATH = "MyFont.glyphspackage"
    TOKEN = "a_github_token_with_repo_permission"
    
    
    OUTLINE_MODE = True
    GLYPH_NAME = "S"
    MASTER_IDX = 1  # 0 for single master
    SAVE_DIR = "~/Desktop"
    SAVE_FORMAT = "mp4"

    ### Don't modify below here

    REPO_URL = f"https://api.github.com/repos/{REPO_OWNER_NAME}/{REPO_NAME}"

    glyph_name_path = (
        GLYPH_NAME if GLYPH_NAME[0].islower() else GLYPH_NAME[0] + "_" + GLYPH_NAME[1:]
    )
    
    glyph_path = f"{GLYPHSPACKAGE_PATH}/glyphs/{glyph_name_path}.glyph"
    fontinfo_path = f"{GLYPHSPACKAGE_PATH}/fontinfo.plist"
    commits_url = f"{REPO_URL}/commits"
    headers = {"Authorization": "TOKEN " + TOKEN}

    glyph_history = get_glyph_history(glyph_path, commits_url, headers, TOKEN, REPO_URL, GLYPH_NAME)
    font= get_fontinfo(fontinfo_path, commits_url,headers,  TOKEN, REPO_URL )

    master_id = font["fontMaster"][MASTER_IDX]["id"]

    draw_glyphs(glyph_history, master_id, font, OUTLINE_MODE, REPO_URL, TOKEN, GLYPHSPACKAGE_PATH)
    
    saveImage(f"{SAVE_DIR}/{GLYPH_NAME}.{SAVE_FORMAT}")


def offCurveColor():
    stroke(0, 0, 0, 0.33)
    fill(0.9, 0.9, 0.9, 1)
    
def curveColor():
    stroke(0, 0, 0, 0.33)
    fill(0,0,0,0)

def cornerColor():
    stroke(0, 0, 0, 0.5)
    fill(0,0,0,0.33)
    
def outlineColor():
    stroke(0, 0, 0, 1)
    fill(0, 0, 0, 0)

def get_fontinfo(fontinfo_path: str,  commits_url: str, headers: dict, TOKEN: str, REPO_URL: str ) -> dict:
    commits_response = requests.get(commits_url, headers=headers)
    if commits_response.status_code == 200:
        latest_commit = commits_response.json()[0]["sha"]
        file_url = f"{REPO_URL}/contents/{fontinfo_path}?ref={latest_commit}"
        file_response = requests.get(file_url, headers=headers)
        if file_response.status_code == 200:
            file_data = file_response.json()
            fontinfo_res = requests.get(file_data["download_url"])
            if fontinfo_res.status_code == 200:
                fontinfo_res.encoding = fontinfo_res.apparent_encoding
                data = fontinfo_res.text
                return loads(data, use_numbers=True)
        else:
            print(f"fontinfo.plist not found at commit {latest_commit}, error")
    else:
        print(
            f"Error {commits_response.status_code} : Could not get the list of commits"
        )


def get_glyph_history(glyph_path: str, commits_url: str, headers: dict, TOKEN: str, REPO_URL: str, GLYPH_NAME: str) -> list:
    commits_response = requests.get(commits_url, headers=headers)
    if commits_response.status_code == 200:
        commits = commits_response.json()
        contents = []
        for commit in commits:
            sha = commit["sha"]
            # Get the file at the specific commit
            file_url = f"{REPO_URL}/contents/{glyph_path}?ref={sha}"
            file_response = requests.get(file_url, headers=headers)
            if file_response.status_code == 200:
                file_data = file_response.json()
                return_content = {
                    'sha': sha,
                    'glyph': loads(
                        base64.b64decode(file_data["content"]).decode(),
                        use_numbers=True)
                }
                contents.append(return_content)                  
                
            else:
                print(f"Glyph {GLYPH_NAME} not found at commit {sha}, skipping")
        return contents
    else:
        print(
            f"Error {commits_response.status_code} : Could not get the list of commits"
        )


def draw_glyphs(glyph_history: list, master_id: str, font: dict, OUTLINE_MODE: bool, REPO_URL: str, TOKEN: str, GLYPHSPACKAGE_PATH: str) -> None:
    em_size = font["unitsPerEm"]
    curve_pt = em_size / 100
    corner_pt = curve_pt
    shape_bin = []
    for glyph in glyph_history:
        for layer in glyph["glyph"]["layers"]:
            if layer["layerId"] == master_id and layer["shapes"] not in shape_bin:
                shape_bin.append(layer["shapes"])
                shape_nodes = [
                    node for shape in layer["shapes"] for node in shape["nodes"]
                ]
                x_coords = [node[0] for node in shape_nodes]
                y_coords = [node[1] for node in shape_nodes]
                hi_x, lo_x = max(x_coords), min(x_coords)
                hi_y, lo_y = max(y_coords), min(y_coords)
                x_translate = (em_size - (hi_x + lo_x)) / 2
                y_translate = (em_size - (hi_y + lo_y)) / 2
                newPage(em_size, em_size)
                fill(1, 1, 1)
                rect(0, 0, width(), height())
                for shape in layer["shapes"]:
                    start = (shape["nodes"][-1][0], shape["nodes"][-1][1])
                    path = BezierPath()
                    path.moveTo(start)
                    for i, node in enumerate(shape["nodes"]):
                        coord = (node[0], node[1])
                        point_type = node[2]
                        if point_type == "o":
                            if OUTLINE_MODE:
                                offCurveColor()
                                if shape["nodes"][i + 1][2] in ("cs", "c"):
                                    line(
                                        (
                                            coord[0] + x_translate,
                                            coord[1] + y_translate,
                                        ),
                                        (
                                            shape["nodes"][i + 1][0] + x_translate,
                                            shape["nodes"][i + 1][1] + y_translate,
                                        ),
                                    )
                                if i > 0 and shape["nodes"][i - 1][2] in ("cs", "c"):
                                    line(
                                        (
                                            coord[0] + x_translate,
                                            coord[1] + y_translate,
                                        ),
                                        (
                                            shape["nodes"][i - 1][0] + x_translate,
                                            shape["nodes"][i - 1][1] + y_translate,
                                        ),
                                    )
                                elif i == 0 and shape["nodes"][-1][2] in ("cs", "c"):
                                    line(
                                        (
                                            coord[0] + x_translate,
                                            coord[1] + y_translate,
                                        ),
                                        (
                                            shape["nodes"][-1][0] + x_translate,
                                            shape["nodes"][-1][1] + y_translate,
                                        ),
                                    )
                                oval(
                                    coord[0] + x_translate - curve_pt / 2,
                                    coord[1] + y_translate - curve_pt / 2,
                                    curve_pt,
                                    curve_pt,
                                )

                        if point_type in ("cs", "c"):
                            pt1 = (shape["nodes"][i - 2][0], shape["nodes"][i - 2][1])
                            pt2 = (shape["nodes"][i - 1][0], shape["nodes"][i - 1][1])
                            pt3 = coord
                            outlineColor()
                            path.curveTo(pt1, pt2, pt3)
                            cornerColor()
                            if OUTLINE_MODE:
                                if point_type == "cs":
                                    oval(
                                        pt3[0] + x_translate - curve_pt / 2,
                                        pt3[1] + y_translate - curve_pt / 2,
                                        curve_pt,
                                        curve_pt,
                                    )
                                elif point_type == "c":
                                    rect(
                                        pt3[0] + x_translate - curve_pt / 2,
                                        pt3[1] + y_translate - curve_pt / 2,
                                        curve_pt,
                                        curve_pt,
                                    )
                        elif point_type == "l":
                            
                            path.lineTo(coord)
                       
                            if OUTLINE_MODE:
                                cornerColor()
                                rect(
                                    coord[0] + x_translate - curve_pt / 2,
                                    coord[1] + y_translate - curve_pt / 2,
                                    curve_pt,
                                    curve_pt,
                                )
                                offCurveColor()
                                if len(shape["nodes"]) > i + 1:
                                    if shape["nodes"][i + 1][2] in ("cs", "c", "o"):
                                        # stroke(0, 0, 0, 0.33)
                                        line(
                                            (
                                                coord[0] + x_translate,
                                                coord[1] + y_translate,
                                            ),
                                            (
                                                shape["nodes"][i + 1][0] + x_translate,
                                                shape["nodes"][i + 1][1] + y_translate,
                                            ),
                                        )

                        elif point_type == "ls":
                            path.lineTo(coord)
                            if OUTLINE_MODE:
                                cornerColor()
                                oval(
                                    coord[0] + x_translate - curve_pt / 2,
                                    coord[1] + y_translate - curve_pt / 2,
                                    curve_pt,
                                    curve_pt,
                                )
                                outlineColor()
                                if shape["nodes"][i + 1][2] in ("cs", "c", "o"):
                                    curveColor()
                                    line(
                                        (
                                            coord[0] + x_translate,
                                            coord[1] + y_translate,
                                        ),
                                        (
                                            shape["nodes"][i + 1][0] + x_translate,
                                            shape["nodes"][i + 1][1] + y_translate,
                                        ),
                                    )

                    if not OUTLINE_MODE:
                        fill(0, 0, 0)
                    else:
                        fill(None)
                    path.closePath()
                    path.translate(x_translate, y_translate)
                    drawPath(path)

main()