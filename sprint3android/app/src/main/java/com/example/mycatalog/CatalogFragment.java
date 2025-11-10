package com.example.mycatalog;

import android.os.Bundle;
import androidx.fragment.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import androidx.navigation.Navigation; // Importar Navigation

public class CatalogFragment extends Fragment {

    public CatalogFragment() {
        // Required empty public constructor
    }

    public static CatalogFragment newInstance(String param1, String param2) {
        CatalogFragment fragment = new CatalogFragment();
        return fragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_catalog, container, false);

        Button btn = rootView.findViewById(R.id.btnDetail);

        if (btn != null) {
            btn.setOnClickListener(view -> {
                Navigation.findNavController(view).navigate(R.id.page_detail);
            });
        }

        return rootView;
    }
}