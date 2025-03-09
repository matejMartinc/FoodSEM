import re


class NelBaseModifier:
    @staticmethod
    def extract_answer(text):
        text = text.replace(' - ', ' # ')
        pattern = r'([a-z0-9\s\-]+\s+[#]\s+(?:http://[a-z-0-9_\.\/]+;)*(?:http://[a-z-0-9_\.\/]+))'
        matches = re.findall(pattern=pattern, string=text, flags=re.IGNORECASE)

        match_found = False
        match = 'Predicted entities: '
        if len(matches) >= 1:
            match_found = True
            for m in matches:
                match += f'{m.replace(' # ', ' - ')}, '
        if match_found and match.endswith(', '):
            match = match[:-2]
        if match_found:
            match = re.sub(pattern=r'\s+', repl=' ', string=match, flags=re.IGNORECASE)
        if not match_found:
            match = ''
        return match

    def clean(self, text):
        text = self.extract_answer(text=text)
        return text


class HansardNelModifier:
    @staticmethod
    def extract_answer(text):
        pattern = r'([a-z0-9\s]+\s*[:-]\s*(?:[a-z0-9\.]+\s\[[^\]]+\];\s?)*(?:[a-z0-9\.]+\s\[[^\]]+\]))'
        matches = re.findall(pattern=pattern, string=text, flags=re.IGNORECASE)

        match_found = False
        match = 'Predicted entities: '
        if len(matches) >= 1:
            match_found = True
            for m in matches:
                m = re.sub(r'\s*\[[^]]+\]', '', m, 1000, re.IGNORECASE)
                match += f'{m.replace(': ', ' - ')}, '
        if match_found and match.endswith(', '):
            match = match[:-2]
        if match_found:
            match = re.sub(pattern=r'\*+', repl=' ', string=match, flags=re.IGNORECASE)
            match = re.sub(pattern=r'\s+', repl=' ', string=match, flags=re.IGNORECASE)
        if not match_found:
            match = ''
        return match

    def clean(self, text):
        text = self.extract_answer(text=text)
        return text


class SaHansardNelModifier:
    @staticmethod
    def extract_answer(text):
        text = text.replace(' - ', ' # ')

        pattern = r'([a-z0-9\s\-()\.]+\s*[#]\s*(?:[a-z0-9\.];\s?)*(?:[a-z0-9\.]+))'

        matches = re.findall(pattern=pattern, string=text, flags=re.IGNORECASE)

        match_found = False
        match = 'Predicted entities: '
        if len(matches) >= 1:
            match_found = True
            for m in matches:
                match += f'{m.replace(': ', ' - ').replace(' # ', ' - ')}, '
        if match_found and match.endswith(', '):
            match = match[:-2]
        if match_found:
            match = re.sub(pattern=r'\*+', repl=' ', string=match, flags=re.IGNORECASE)
            match = re.sub(pattern=r'\s+', repl=' ', string=match, flags=re.IGNORECASE)
        if not match_found:
            match = ''
        return match

    def clean(self, text):
        text = self.extract_answer(text=text)
        return text

class FoodOnNelExtendedModifier:
    @staticmethod
    def extract_answer(text):
        text = text.replace(' - ', ' # ')
        pattern = r'(\**[a-z0-9\s\-]+\**\s*[:#]\s*\**\s*(?:http[s]?://[a-z-0-9_\.\/#?:=]+;)*(?:http[s]?://[a-z-0-9_\.\/#?:=]+))'
        matches = re.findall(pattern=pattern, string=text, flags=re.IGNORECASE)

        pattern_2 = r'(\**[a-z0-9\s\-]+\**\s*[:#]\s*(?:\[[a-z0-9:\s_\-#\/\.]+\]\(http[s]?://[a-z-0-9_\.\/:#?=]+\))*\[[a-z0-9:\s_\-#\/\.]+\]\(http[s]?://[a-z-0-9_\.\/:#?=]+\))'
        matches_2 = re.findall(pattern=pattern_2, string=text, flags=re.IGNORECASE)

        pattern_3 = r'(\**[a-z0-9\s\-]+\**\s*[:#]\s*(?:[<`]?http://[a-z-0-9_\.\/#?:=]+[`>]?;)*(?:[`<]?http://[a-z-0-9_\.\/#?:=]+[`>]?))'
        matches_3 = re.findall(pattern=pattern_3, string=text, flags=re.IGNORECASE)

        pattern_4 = r'(\**[a-z0-9\s\-]+\**\s*[:#]\s*`[a-z0-9:_\s]+`\s*.\s*[\[\(]?http[s]?://[a-z-0-9_\.\/:#?=]+[\]\)]?)'
        matches_4 = re.findall(pattern=pattern_4, string=text, flags=re.IGNORECASE)

        pattern_5 = r'(\*+[a-z0-9\s\-]+\*+\s*[:#]\s*[a-z0-9:_\s]+[\[\(]?http[s]?://[a-z-0-9_\.\/:#?=]+[\]\)]?)'
        matches_5 = re.findall(pattern=pattern_5, string=text, flags=re.IGNORECASE)

        pattern_6 = r'(\**[a-z0-9\s\-]+\**\s*[:#]\s*`[a-z0-9:_\s]+`\s*.\s*[\[\(][a-z0-9\s]+[\]\)]\s*[\[\(]?http[s]?://[a-z-0-9_\.\/:#?=]+[\]\)]?)'
        matches_6 = re.findall(pattern=pattern_6, string=text, flags=re.IGNORECASE)

        pattern_7 = r'(\**[a-z0-9\s\-]+\**\s*[:#]\s+[a-z0-9]+:[a-z0-9]+\s+(?:http[s]?://[a-z0-9_\.\/#?:=]+;)*(?:http[s]?://[a-z0-9_\.\/#?:=]+))'
        matches_7 = re.findall(pattern=pattern_7, string=text, flags=re.IGNORECASE)

        match_found = False
        match = 'Predicted entities: '

        if len(matches_2) >= 1:
            match_found = True
            for m in matches_2:
                m = re.sub(pattern=r'\[[a-z0-9:\s_\-#\/\.]+\]', repl=' ', string=m, flags=re.IGNORECASE)
                match += f'{m.replace(': ', ' - ').replace(' # ', ' - ').replace(
                    '(', '').replace(')', '').replace('*', '')}, '
        elif len(matches_3) >= 1:
            match_found = True
            for m in matches_3:
                match += f'{m.replace(': ', ' - ').replace(' # ', ' - ').replace('`', '')}, '
        elif len(matches_4) >= 1:
            match_found = True
            for m in matches_4:
                m = re.sub(pattern=r'`[a-z0-9:_\s]+`\s*.\s*', repl=' ', string=m, flags=re.IGNORECASE)
                match += f'{m.replace(': ', ' - ').replace(' # ', ' - ').replace(
                    '(', '').replace(')', '').replace('*', '').replace('`', '')}, '
        elif len(matches_5) >= 1:
            match_found = True
            for m in matches_5:
                m = re.sub(pattern=r'[:#]\s*[a-z0-9:_\s]+[\[\(]', repl=' ', string=m, flags=re.IGNORECASE)
                match += f'{m.replace('** ', ' - ').replace(' # ', ' - ').replace(
                    '(', '').replace(')', '').replace('*', '').replace('`', '')}, '
        elif len(matches_6) >= 1:
            match_found = True
            for m in matches_6:
                m = re.sub(pattern=r'`[a-z0-9:_\s]+`\s*.\s*[\[\(][a-z0-9\s]+[\]\)]', repl=' ', string=m, flags=re.IGNORECASE)
                match += f'{m.replace(': ', ' - ').replace(' # ', ' - ').replace(
                    '(', '').replace(')', '').replace('*', '').replace('`', '')}, '
        elif len(matches_7) >= 1:
            match_found = True
            for m in matches_7:
                m = re.sub(pattern=r'\s+[a-z0-9]+:[a-z0-9]+\s+', repl=' ', string=m, flags=re.IGNORECASE)
                match += f'{m.replace(': ', ' - ').replace(' # ', ' - ').replace(
                    '(', '').replace(')', '').replace('*', '').replace(
                    '`', '')}, '
        elif len(matches) >= 1:
            match_found = True
            for m in matches:
                match += f'{m.replace(': ', ' - ').replace(' # ', ' - ').replace('*', '')}, '
        if match_found and match.endswith(', '):
            match = match[:-2]
        if match_found:
            match = re.sub(pattern=r'\*+', repl=' ', string=match, flags=re.IGNORECASE)
            match = re.sub(pattern=r'\s+', repl=' ', string=match, flags=re.IGNORECASE)
        if not match_found:
            match = ''
        return match

    def clean(self, text):
        text = self.extract_answer(text=text)
        return text


class SnomedNelExtendedModifier:
    @staticmethod
    def extract_answer(text):
        text = text.replace(' - ', ' # ')
        pattern = r'(\**[a-z0-9\s\-]+\**\s*[:#]\s*\**\s*(?:http[s]?://[a-z-0-9_\.\/#?:=]+;)*(?:http[s]?://[a-z-0-9_\.\/#?:=]+))'
        matches = re.findall(pattern=pattern, string=text, flags=re.IGNORECASE)

        pattern_1 = r'([0-9]+\.\s+\**([a-z0-9\s\-]+)\**\s*[:#]\s*[^=]+[\[\(]?(http[s]?://[a-z-0-9_\.\/:#?=&\s]+)[\]\)]?)'
        matches_1 = re.findall(pattern=pattern_1, string=text, flags=re.IGNORECASE)

        pattern_2 = r'(\*+[a-z0-9\s\-]+\*+\s*[:#]\s*[a-z0-9:_\s]+[\[\(]?http[s]?://[a-z-0-9_\.\/:#?=]+[\]\)]?)'
        matches_2 = re.findall(pattern=pattern_2, string=text, flags=re.IGNORECASE)

        pattern_3 = r'(\**[a-z0-9\s\-]+\**\s*[:#]\s+[\[\(]?[a-z0-9\s]+:\s*[a-z0-9]+[\]\)]?\s*(?:[\[\(]?http[s]?://[a-z-0-9_\.\/:#?=&]+[\]\)]?;)*(?:[\[\(]?http[s]?://[a-z-0-9_\.\/:#?=&]+[\]\)]?))'
        matches_3 = re.findall(pattern=pattern_3, string=text, flags=re.IGNORECASE)

        pattern_4 = r'(\**[a-z0-9\s\-]+\**\s*[:#]\s+[a-z0-9\s]+:?[a-z0-9]+\s+(?:http[s]?://[a-z0-9_\.\/#?:=]+;)*(?:http[s]?://[a-z0-9_\.\/#?:=]+))'
        matches_4 = re.findall(pattern=pattern_4, string=text, flags=re.IGNORECASE)

        match_found = False
        match = 'Predicted entities: '

        if len(matches_2) >= 1:
            match_found = True
            for m in matches_2:
                m = re.sub(pattern=r'[:#]\s*[a-z0-9:_\s]+[\[\(]', repl=' ', string=m, flags=re.IGNORECASE)
                match += f'{m.replace('** ', ' - ').replace(' # ', ' - ').replace(
                    '(', '').replace(')', '').replace('*', '').replace('`', '')}, '
        elif len(matches_3) >= 1:
            match_found = True
            for m in matches_3:
                m = re.sub(pattern=r'[\[\(]?[a-z0-9\s]+:\s*[a-z0-9]+[\]\)]?', repl=' ', string=m, flags=re.IGNORECASE)
                match += f'{m.replace(': ', ' - ').replace(' # ', ' - ').replace(
                    '(', '').replace(')', '').replace('*', '').replace('`', '')}, '
        elif len(matches_4) >= 1:
            match_found = True
            for m in matches_4:
                m = re.sub(pattern=r'\s+[a-z0-9]+:[a-z0-9]+\s+', repl=' ', string=m, flags=re.IGNORECASE)
                match += f'{m.replace(': ', ' - ').replace(' # ', ' - ').replace(
                    '(', '').replace(')', '').replace('*', '').replace('`', '')}, '
        elif len(matches) >= 1:
            match_found = True
            for m in matches:
                match += f'{m.replace(': ', ' - ').replace(' # ', ' - ').replace('*', '')}, '
        elif len(matches_1) >= 1:
            match_found = True
            for m in matches_1:
                m = m[1] + ' - ' + m[2]
                match += f'{m.replace(': ', ' - ').replace(' # ', ' - ').replace('(', '').replace(
                    ')', '').replace('*', '').replace('`', '')}, '
        if match_found and match.endswith(', '):
            match = match[:-2]
        if match_found:
            match = re.sub(pattern=r'\*+', repl=' ', string=match, flags=re.IGNORECASE)
            match = re.sub(pattern=r'\s+', repl=' ', string=match, flags=re.IGNORECASE)
        if not match_found:
            match = ''
        return match

    def clean(self, text):
        text = self.extract_answer(text=text)
        return text
