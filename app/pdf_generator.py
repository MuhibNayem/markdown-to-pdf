import mistune
from datetime import datetime
import json
import os
import re
import weasyprint

class PDFGenerator:
    @staticmethod
    def create_pdf(content: str, filename: str) -> str:
        try:
            data = json.loads(content)
            summary = data.get('summary', '')
        except json.JSONDecodeError:
            summary = content
        
        summary = PDFGenerator.preprocess_markdown(summary)
        
        markdown = mistune.create_markdown()
        html_content = markdown(summary)
        
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{output_dir}/{filename}_{timestamp}.pdf"
        
        weasyprint.HTML(string=html_content).write_pdf(output_path)
        
        return output_path
    
    @staticmethod
    def preprocess_markdown(text):
        text = re.sub(r'###\s+####\s+', '### ', text)
        
        lines = text.split('\n')
        processed_lines = []
        indent_stack = []
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('#'):
                indent_stack = []
                processed_lines.append(line)
                continue
            
            if stripped.startswith('-'):
                indent = len(line) - len(stripped)
                
                while indent_stack and indent_stack[-1] >= indent:
                    indent_stack.pop()

                if not indent_stack or indent > indent_stack[-1]:
                    indent_stack.append(indent)

                indent_level = len(indent_stack)
                indent_spaces = '  ' * (indent_level - 1)
                processed_lines.append(f"{indent_spaces}{stripped}")
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
