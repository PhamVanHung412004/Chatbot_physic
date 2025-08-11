import re
from typing import (
    Dict
)
def latex_to_text(latex_formula : str) -> str:
    """
    Chuyển đổi công thức LaTeX sang text thông thường
    Hỗ trợ đầy đủ các ký hiệu toán học và vật lý
    """
    # Tạo bản sao để xử lý
    text : str = latex_formula
    
    # Dictionary chứa các phép chuyển đổi
    replacements : Dict[str, str] = {
        # === TOÁN HỌC CƠ BẢN ===
        # Phân số
        r'\\frac\{([^}]+)\}\{([^}]+)\}': r'(\1)/(\2)',
        
        # Căn
        r'\\sqrt\{([^}]+)\}': r'√(\1)',
        r'\\sqrt\[([^\]]+)\]\{([^}]+)\}': r'\1√(\2)',  # Căn bậc n
        
        # Lũy thừa và chỉ số
        r'\^(\d)': r'^(\1)',  # Số đơn
        r'\^\{([^}]+)\}': r'^(\1)',  # Biểu thức phức tạp
        r'_(\d)': r'_\1',  # Chỉ số dưới đơn
        r'_\{([^}]+)\}': r'_(\1)',  # Chỉ số dưới phức tạp
        
        # === KÝ HIỆU HY LẠP ===
        r'\\alpha': 'α',
        r'\\beta': 'β',
        r'\\gamma': 'γ',
        r'\\delta': 'δ',
        r'\\epsilon': 'ε',
        r'\\varepsilon': 'ε',
        r'\\zeta': 'ζ',
        r'\\eta': 'η',
        r'\\theta': 'θ',
        r'\\vartheta': 'ϑ',
        r'\\iota': 'ι',
        r'\\kappa': 'κ',
        r'\\lambda': 'λ',
        r'\\mu': 'μ',
        r'\\nu': 'ν',
        r'\\xi': 'ξ',
        r'\\pi': 'π',
        r'\\rho': 'ρ',
        r'\\sigma': 'σ',
        r'\\tau': 'τ',
        r'\\upsilon': 'υ',
        r'\\phi': 'φ',
        r'\\varphi': 'φ',
        r'\\chi': 'χ',
        r'\\psi': 'ψ',
        r'\\omega': 'ω',
        # Chữ hoa
        r'\\Gamma': 'Γ',
        r'\\Delta': 'Δ',
        r'\\Theta': 'Θ',
        r'\\Lambda': 'Λ',
        r'\\Xi': 'Ξ',
        r'\\Pi': 'Π',
        r'\\Sigma': 'Σ',
        r'\\Upsilon': 'Υ',
        r'\\Phi': 'Φ',
        r'\\Psi': 'Ψ',
        r'\\Omega': 'Ω',
        
        # === TOÁN TỬ TOÁN HỌC ===
        r'\\times': '×',
        r'\\div': '÷',
        r'\\pm': '±',
        r'\\mp': '∓',
        r'\\cdot': '·',
        r'\\bullet': '•',
        r'\\circ': '○',
        r'\\infty': '∞',
        r'\\approx': '≈',
        r'\\neq': '≠',
        r'\\equiv': '≡',
        r'\\leq': '≤',
        r'\\geq': '≥',
        r'\\ll': '≪',
        r'\\gg': '≫',
        r'\\sim': '∼',
        r'\\simeq': '≃',
        r'\\propto': '∝',
        r'\\rightarrow': '→',
        r'\\leftarrow': '←',
        r'\\leftrightarrow': '↔',
        r'\\Rightarrow': '⇒',
        r'\\Leftarrow': '⇐',
        r'\\Leftrightarrow': '⇔',
        r'\\uparrow': '↑',
        r'\\downarrow': '↓',
        r'\\updownarrow': '↕',
        
        # === ĐẠO HÀM VÀ VI PHÂN ===
        r'\\partial': '∂',
        r'\\nabla': '∇',
        r'\\Delta': 'Δ',
        r'\\prime': '′',
        r'\\dot\{([^}]+)\}': r'\1̇',  # Đạo hàm theo thời gian
        r'\\ddot\{([^}]+)\}': r'\1̈',  # Đạo hàm bậc 2 theo thời gian
        r'\\frac\{d([^}]+)\}\{d([^}]+)\}': r'd\1/d\2',  # Đạo hàm thường
        r'\\frac\{d\^2([^}]+)\}\{d([^}]+)\^2\}': r'd²\1/d\2²',  # Đạo hàm bậc 2
        r'\\frac\{\\partial([^}]+)\}\{\\partial([^}]+)\}': r'∂\1/∂\2',  # Đạo hàm riêng
        
        # === TÍCH PHÂN ===
        r'\\int': '∫',
        r'\\oint': '∮',
        r'\\iint': '∬',
        r'\\iiint': '∭',
        
        # === TỔNG VÀ TÍCH ===
        r'\\sum': 'Σ',
        r'\\prod': 'Π',
        r'\\coprod': '∐',
        
        # === VECTOR VÀ TENSOR ===
        r'\\vec\{([^}]+)\}': r'\1⃗',  # Vector
        r'\\overrightarrow\{([^}]+)\}': r'\1⃗',
        r'\\mathbf\{([^}]+)\}': r'𝐛(\1)',  # Bold vector
        r'\\boldsymbol\{([^}]+)\}': r'𝜷(\1)',
        r'\\hat\{([^}]+)\}': r'\1̂',  # Unit vector
        r'\\tilde\{([^}]+)\}': r'\1̃',
        r'\\bar\{([^}]+)\}': r'\1̄',
        r'\\overline\{([^}]+)\}': r'\1̅',
        r'\\underline\{([^}]+)\}': r'\1̲',
        
        # === KÝ HIỆU VẬT LÝ ĐẶC BIỆT ===
        r'\\hbar': 'ℏ',  # h-bar (hằng số Planck rút gọn)
        r'\\ell': 'ℓ',  # l viết cong
        r'\\Re': 'ℜ',  # Phần thực
        r'\\Im': 'ℑ',  # Phần ảo
        r'\\aleph': 'ℵ',
        r'\\wp': '℘',
        r'\\emptyset': '∅',
        r'\\varnothing': '∅',
        r'\\angle': '∠',
        r'\\measuredangle': '∡',
        r'\\sphericalangle': '∢',
        r'\\parallel': '∥',
        r'\\perp': '⊥',
        r'\\bot': '⊥',
        
        # === LƯỢNG GIÁC ===
        r'\\sin': 'sin',
        r'\\cos': 'cos',
        r'\\tan': 'tan',
        r'\\cot': 'cot',
        r'\\sec': 'sec',
        r'\\csc': 'csc',
        r'\\arcsin': 'arcsin',
        r'\\arccos': 'arccos',
        r'\\arctan': 'arctan',
        r'\\sinh': 'sinh',
        r'\\cosh': 'cosh',
        r'\\tanh': 'tanh',
        
        # === LOGARIT VÀ MŨ ===
        r'\\log': 'log',
        r'\\ln': 'ln',
        r'\\lg': 'lg',
        r'\\exp': 'exp',
        
        # === GIỚI HẠN VÀ CÁC HÀM ===
        r'\\lim': 'lim',
        r'\\sup': 'sup',
        r'\\inf': 'inf',
        r'\\max': 'max',
        r'\\min': 'min',
        r'\\det': 'det',
        r'\\dim': 'dim',
        r'\\deg': 'deg',
        r'\\ker': 'ker',
        r'\\tr': 'tr',
        
        # === TẬP HỢP ===
        r'\\in': '∈',
        r'\\notin': '∉',
        r'\\subset': '⊂',
        r'\\supset': '⊃',
        r'\\subseteq': '⊆',
        r'\\supseteq': '⊇',
        r'\\cup': '∪',
        r'\\cap': '∩',
        r'\\setminus': '∖',
        r'\\forall': '∀',
        r'\\exists': '∃',
        r'\\nexists': '∄',
        r'\\therefore': '∴',
        r'\\because': '∵',
        
        # === MA TRẬN VÀ DẤU NGOẶC ===
        r'\\begin\{pmatrix\}': '(',
        r'\\end\{pmatrix\}': ')',
        r'\\begin\{bmatrix\}': '[',
        r'\\end\{bmatrix\}': ']',
        r'\\begin\{vmatrix\}': '|',
        r'\\end\{vmatrix\}': '|',
        r'\\begin\{Vmatrix\}': '‖',
        r'\\end\{Vmatrix\}': '‖',
        r'\\left\(': '(',
        r'\\right\)': ')',
        r'\\left\[': '[',
        r'\\right\]': ']',
        r'\\left\{': '{',
        r'\\right\}': '}',
        r'\\left\|': '‖',
        r'\\right\|': '‖',
        r'\\langle': '⟨',
        r'\\rangle': '⟩',
        r'\\{': '{',
        r'\\}': '}',
        
        # === ĐƠN VỊ VẬT LÝ (SI) ===
        r'\\mathrm\{kg\}': 'kg',
        r'\\mathrm\{m\}': 'm',
        r'\\mathrm\{s\}': 's',
        r'\\mathrm\{A\}': 'A',
        r'\\mathrm\{K\}': 'K',
        r'\\mathrm\{mol\}': 'mol',
        r'\\mathrm\{cd\}': 'cd',
        r'\\mathrm\{Hz\}': 'Hz',
        r'\\mathrm\{N\}': 'N',
        r'\\mathrm\{Pa\}': 'Pa',
        r'\\mathrm\{J\}': 'J',
        r'\\mathrm\{W\}': 'W',
        r'\\mathrm\{C\}': 'C',
        r'\\mathrm\{V\}': 'V',
        r'\\mathrm\{F\}': 'F',
        r'\\mathrm\{Ω\}': 'Ω',
        r'\\mathrm\{S\}': 'S',
        r'\\mathrm\{Wb\}': 'Wb',
        r'\\mathrm\{T\}': 'T',
        r'\\mathrm\{H\}': 'H',
        r'\\mathrm\{°C\}': '°C',
        r'\\mathrm\{lm\}': 'lm',
        r'\\mathrm\{lx\}': 'lx',
        r'\\mathrm\{Bq\}': 'Bq',
        r'\\mathrm\{Gy\}': 'Gy',
        r'\\mathrm\{Sv\}': 'Sv',
        r'\\mathrm\{eV\}': 'eV',
        
        # === CÁC KÝ HIỆU KHÁC ===
        r'\\&': '&',
        r'\\%': '%',
        r'\\#': '#',
        r'\\S': '§',
        r'\\dagger': '†',
        r'\\ddagger': '‡',
        r'\\star': '★',
        r'\\ast': '*',
        r'\\oplus': '⊕',
        r'\\ominus': '⊖',
        r'\\otimes': '⊗',
        r'\\oslash': '⊘',
        r'\\odot': '⊙',
        r'\\bigcirc': '○',
        r'\\square': '□',
        r'\\blacksquare': '■',
        r'\\triangle': '△',
        r'\\blacktriangle': '▲',
        r'\\nabla': '∇',
        r'\\diamondsuit': '♦',
        r'\\heartsuit': '♥',
        r'\\clubsuit': '♣',
        r'\\spadesuit': '♠',
        
        # === KHOẢNG TRẮNG VÀ ĐỊNH DẠNG ===
        r'\\,': ' ',
        r'\\:': '  ',
        r'\\;': '   ',
        r'\\!': '',
        r'\\quad': '    ',
        r'\\qquad': '        ',
        r'\\\\': '\n',  # Xuống dòng
        r'\\text\{([^}]+)\}': r'\1',  # Text thường
        r'\\mathrm\{([^}]+)\}': r'\1',  # Roman
        r'\\mathit\{([^}]+)\}': r'\1',  # In nghiêng
        r'\\mathbb\{([^}]+)\}': r'𝔹(\1)',  # Blackboard bold
        r'\\mathcal\{([^}]+)\}': r'𝒞(\1)',  # Calligraphy
        r'\\mathfrak\{([^}]+)\}': r'𝔉(\1)',  # Fraktur
        
        # === XỬ LÝ BẢNG ===
        r'\\begin\{array\}.*?': '',
        r'\\end\{array\}': '',
        r'&': ' | ',  # Phân cách cột
    }
    
    # Áp dụng các phép thay thế
    for pattern, replacement in replacements.items():
        text : str = re.sub(pattern, replacement, text)
    
    # === XỬ LÝ ĐẶC BIỆT ===
    
    # Chuyển đổi chỉ số trên (superscript)
    superscripts : Dict[str, str] = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
        'n': 'ⁿ', 'i': 'ⁱ', 'x': 'ˣ', 'y': 'ʸ', 'z': 'ᶻ',
        'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ', 'e': 'ᵉ',
        'f': 'ᶠ', 'g': 'ᵍ', 'h': 'ʰ', 'j': 'ʲ', 'k': 'ᵏ',
        'l': 'ˡ', 'm': 'ᵐ', 'o': 'ᵒ', 'p': 'ᵖ', 'r': 'ʳ',
        's': 'ˢ', 't': 'ᵗ', 'u': 'ᵘ', 'v': 'ᵛ', 'w': 'ʷ'
    }
    
    # Chuyển đổi chỉ số dưới (subscript)
    subscripts : str = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
        '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
        'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ', 'i': 'ᵢ', 'j': 'ⱼ',
        'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ',
        'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ',
        'v': 'ᵥ', 'x': 'ₓ'
    }
    
    # Xử lý lũy thừa
    def replace_superscript(match):
        exp : str = match.group(1)
        result : str = ''
        for char in exp:
            result += superscripts.get(char, char)
        if result == exp:  # Nếu không chuyển được hết
            return f'^({exp})'
        return result
    
    # Xử lý chỉ số dưới
    def replace_subscript(match):
        sub : str = match.group(1)
        result : str = ''
        for char in sub:
            result += subscripts.get(char, char)
        if result == sub:  # Nếu không chuyển được hết
            return f'_({sub})'
        return result
    
    # Áp dụng chuyển đổi superscript và subscript
    text : str = re.sub(r'\^\(([^)]+)\)', lambda m: replace_superscript(m), text)
    text : str = re.sub(r'\^(\w)', lambda m: superscripts.get(m.group(1), f'^{m.group(1)}'), text)
    text : str = re.sub(r'_\(([^)]+)\)', lambda m: replace_subscript(m), text)
    text : str = re.sub(r'_(\w)', lambda m: subscripts.get(m.group(1), f'_{m.group(1)}'), text)
    
    # Xóa dấu $ và các ký tự LaTeX còn lại
    text : str = text.replace('$', '')
    text : str = re.sub(r'\\[a-zA-Z]+', '', text)  # Xóa các lệnh LaTeX không xử lý
    
    # Làm sạch khoảng trắng thừa
    text : str = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Hàm tiện ích
def convert(latex_formula : str) -> str:
    """Hàm đơn giản để chuyển đổi nhanh"""
    return latex_to_text(latex_formula)
