#include <clang/Basic/Version.h>
#include <clang/Basic/TokenKinds.h>
#include <llvm/ADT/StringRef.h>
#include <iostream>

int main() {
    std::cout << "Clang full version: " << clang::getClangFullVersion() << "\n";

    clang::tok::TokenKind tk = clang::tok::kw_if;
    const char* name = clang::tok::getTokenName(tk);
    std::cout << "Sample token name: " << name << "\n";

    llvm::StringRef sr(name);
    std::cout << "Length via StringRef: " << sr.size() << "\n";

    return 0;
}
