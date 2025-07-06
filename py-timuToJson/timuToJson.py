import tkinter as tk
from tkinter import filedialog
import re, time, random, json, os

def process_txt_file(file_path):
    """处理单个TXT文件并返回题目列表"""
    with open(file_path, 'r', encoding='UTF-8') as f:
        data = f.read()
    
    data = data.replace('．', '.')
    
    # 不同题目分割
    pattern = re.compile(r'(?:^|\n\s*)\d+?[\.\。]')
    questions = pattern.split(data)
    
    result = []
    for i in questions:
        if not i.strip():  # 跳过空题目
            continue
            
        pattern = re.compile(r'\n')
        # 题目
        title = pattern.split(i)[0]
        
        # 替换题目中的连续空格为下划线
        title = re.sub(r' {4,}', '__________', title)
        
        # 选项
        option = re.findall(r'[A-E][\.\。]?(.+?)\s+[\n]?', i)
        
        # 答案
        daan = re.findall(r'答案[:：]([A-E]+)[\n]?', i)
        analysis = ''
        
                # 在process_txt_file函数中修改这部分逻辑
        # 判断题目类型
        question_type = 'fill'  # 默认设为填空题

        # 1. 先检查是否是判断题
        if len(option) == 2:
            has_correct = any('正确' in opt for opt in option)
            has_wrong = any('错误' in opt for opt in option)
            if has_correct and has_wrong:
                question_type = 'judge'

        # 2. 如果不是判断题，检查是否是选择题
        if question_type == 'fill' and len(option) > 0:
            question_type = 'choice'

        # 3. 处理答案和解析
        if len(daan) == 0:
            daan = re.findall(r'答案[:：]([\s\S]+)', i)
            if len(daan):
                pattern = re.compile(r'解析[:：]')
                daanList = pattern.split(daan[0])
                if len(daanList) > 1:
                    analysis = daanList[1]
                    daan = [daanList[0]]
                
                # 如果是填空题/简答题，确定具体类型
                if question_type != 'judge':
                    daan_text = daan[0] if len(daan) else ''
                    if len(daan_text) > 16:
                        question_type = 'short_answer'
                    else:
                        question_type = 'fill'
                    
                    daan = [daan_text.replace(' ', '_')]
        else:
            # 选择题获取解析
            jiexi = re.findall(r'解析[:：]([\s\S]+)', i)
            analysis = jiexi[0] if len(jiexi) else ''
        
        daan = daan[0] if len(daan) else ''

        result.append({
            'id': f"{time.strftime('%Y%m%d%H%M', time.localtime())}{random.randint(0, 1000000)}",
            'type': question_type,
            'title': title,
            'option': option,
            'answer': daan,
            'analysis': analysis.strip() if analysis else ''
        })
    
    return result

def main():
    root = tk.Tk()
    root.withdraw()
    
    # 选择多个TXT文件
    file_paths = filedialog.askopenfilenames(
        title='选择要转换的TXT文件',
        filetypes=[('文本文件', '*.txt'), ('所有文件', '*.*')]
    )
    
    if not file_paths:
        print("❌ 没有选择文件")
        return
    
    # 创建输出目录
    output_dir = os.path.join(os.getcwd(), "json_output")
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理每个文件
    for file_path in file_paths:
        try:
            # 处理文件
            questions = process_txt_file(file_path)
            
            if not questions:
                print(f"⚠️ 文件 {os.path.basename(file_path)} 中没有找到有效题目")
                continue
            
            # 生成输出文件名
            filename = os.path.basename(file_path).replace('.txt', '') + '.json'
            output_path = os.path.join(output_dir, filename)
            
            # 写入JSON文件
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(questions, f, ensure_ascii=False, indent=4)
            
            print(f"✅ 成功转换: {os.path.basename(file_path)} → {filename}")
            print(f"   保存路径: {os.path.abspath(output_path)}")
            print(f"   题目数量: {len(questions)}")
            
        except Exception as e:
            print(f"❌ 处理文件 {os.path.basename(file_path)} 时出错: {str(e)}")
    
    print("\n🎉 批量转换完成!")
    print(f"所有JSON文件已保存到: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()