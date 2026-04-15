// Copyright (c) 2023 Saturn Developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include "nontrivial-threadlocal.h"

#include <clang-tidy/ClangTidyModule.h>

class SaturnModule final : public clang::tidy::ClangTidyModule
{
public:
    void addCheckFactories(clang::tidy::ClangTidyCheckFactories& CheckFactories) override
    {
        CheckFactories.registerCheck<saturn::NonTrivialThreadLocal>("saturn-nontrivial-threadlocal");
    }
};

static clang::tidy::ClangTidyModuleRegistry::Add<SaturnModule>
    X("saturn-module", "Adds saturn checks.");

volatile int SaturnModuleAnchorSource = 0;
